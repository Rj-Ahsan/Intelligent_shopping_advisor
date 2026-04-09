from sqlalchemy.orm import Session
from models.product import Product
from utils.vector_store import search_similar_products
from agents.preference_agent import Preferences

def retrieve_products(preferences: Preferences, db: Session, index=None, products=None):
    try:
        query = f"{preferences.category or ''} {' '.join(preferences.key_features or [])}"
        
        if index and products:
            candidates = search_similar_products(query, index, products, None)
        else:
            candidates = db.query(Product).filter(Product.category == preferences.category).all() if preferences.category else db.query(Product).all()
        
        if preferences.budget:
            candidates = [p for p in candidates if p.price <= preferences.budget]
        
        return candidates[:20]  # Limit
    except Exception as e:
        print(f"Error in retrieve_products: {e}")
        return []