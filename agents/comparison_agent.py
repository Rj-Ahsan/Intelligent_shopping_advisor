from typing import List
from models.product import Product

def compare_products(products: List[Product]) -> List[dict]:
    if not products:
        return []
    
    try:
        comparisons = []
        for p in products:
            # Avoid division by zero
            price_factor = (1 / p.price * 100) if p.price > 0 else 0
            score = (p.rating_rate * 0.5) + price_factor if p.rating_rate else 0
            comparisons.append({
                "product": p,
                "score": score
            })
        comparisons.sort(key=lambda x: x["score"], reverse=True)
        return comparisons
    except Exception as e:
        print(f"Error in compare_products: {e}")
        return []