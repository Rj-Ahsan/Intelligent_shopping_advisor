import requests
import json
from pathlib import Path
from sqlalchemy.orm import Session
from models.product import Product

def fetch_products():
    url = "https://fakestoreapi.com/products"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Warning: Failed to fetch products from API: {e}")
        return _load_fallback_products()


def _load_fallback_products():
    fallback_path = Path(__file__).resolve().parent.parent / "data" / "products_fallback.json"
    if not fallback_path.exists():
        return []
    try:
        with open(fallback_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Warning: Failed to load fallback products: {e}")
        return []

def load_products_to_db(db: Session):
    # Check if products already exist
    existing_count = db.query(Product).count()
    if existing_count > 0:
        print(f"Database already has {existing_count} products, skipping load")
        return
    
    products_data = fetch_products()
    if not products_data:
        print("No products to load - API unavailable or no data returned")
        return
        
    for item in products_data:
        product = Product(
            id=item['id'],
            title=item['title'],
            price=item['price'],
            description=item['description'],
            category=item['category'],
            image=item['image'],
            rating_rate=item['rating']['rate'],
            rating_count=item['rating']['count']
        )
        db.add(product)
    db.commit()
    print(f"Loaded {len(products_data)} products into database")