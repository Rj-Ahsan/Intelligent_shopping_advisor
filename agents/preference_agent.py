import re
from pydantic import BaseModel, Field
from typing import Optional, List

class Preferences(BaseModel):
    budget: Optional[float] = None
    category: Optional[str] = None
    key_features: List[str] = Field(default_factory=list)

def extract_preferences(query: str) -> Preferences:
    if not query:
        return Preferences()
    
    try:
        query_lower = query.lower()
        budget = _extract_budget(query_lower)
        category = _extract_category(query_lower)
        key_features = []
        feature_keywords = [
            "gaming", "battery", "performance", "camera", "lightweight",
            "durable", "office", "student", "programming", "casual"
        ]
        for keyword in feature_keywords:
            if keyword in query_lower:
                key_features.append(keyword)
        return Preferences(budget=budget, category=category, key_features=key_features)
    except Exception as e:
        print(f"Error extracting preferences: {e}")
        return Preferences()


def _extract_budget(query_lower: str) -> Optional[float]:
    # Supports: "under 100000", "below 500", "budget 1500", "PKR 100000"
    budget_patterns = [
        r"(?:under|below|less than|budget)\s*(?:pkr|rs\.?|usd|\$)?\s*(\d+(?:\.\d+)?)",
        r"(?:pkr|rs\.?|usd|\$)\s*(\d+(?:\.\d+)?)",
    ]

    for pattern in budget_patterns:
        match = re.search(pattern, query_lower, flags=re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue
    return None


def _extract_category(query_lower: str) -> Optional[str]:
    if any(term in query_lower for term in ["phone", "smartphone", "mobile", "laptop", "tablet", "electronics"]):
        return "electronics"
    if any(term in query_lower for term in ["jewel", "ring", "necklace", "bracelet"]):
        return "jewelery"
    if any(term in query_lower for term in ["men", "shirt", "jacket", "male clothing"]):
        return "men's clothing"
    if any(term in query_lower for term in ["women", "dress", "female clothing"]):
        return "women's clothing"
    return None