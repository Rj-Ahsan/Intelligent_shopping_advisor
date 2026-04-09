from typing import List

def recommend_products(comparisons: List[dict], top_n=5) -> List[dict]:
    if not comparisons:
        return []
    
    try:
        top = comparisons[:top_n]
        recommendations = []
        for comp in top:
            p = comp.get("product")
            if p:
                justification = f"High rating ({p.rating_rate}) and good value for price (${p.price})."
                recommendations.append({
                    "title": p.title,
                    "price": p.price,
                    "description": p.description,
                    "rating": p.rating_rate,
                    "justification": justification
                })
        return recommendations
    except Exception as e:
        print(f"Error in recommend_products: {e}")
        return []