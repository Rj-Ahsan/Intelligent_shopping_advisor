#!/usr/bin/env python
"""Simple test to verify the system components work"""

print("Starting simple test...")

# Test 1: Database and data loading
print("\n[1/4] Testing database and data loading...")
from database.connection import SessionLocal, engine
from models.product import Product
from utils.data_loader import load_products_to_db

db = SessionLocal()
print(f"  - Database connection: OK")

load_products_to_db(db)
product_count = db.query(Product).count()
print(f"  - Products loaded: {product_count} products")

# Test 2: Agent components
print("\n[2/4] Testing preference extraction...")
from agents.preference_agent import extract_preferences

prefs = extract_preferences("Best smartphone under 100")
print(f"  - Extracted preferences: {prefs}")

# Test 3: Product retrieval
print("\n[3/4] Testing product retrieval...")
from agents.product_retrieval_agent import retrieve_products

products = retrieve_products(prefs, db)
print(f"  - Retrieved {len(products)} products matching preferences")
if products:
    print(f"    Sample: {products[0].title} - ${products[0].price}")

# Test 4: Comparison and recommendation
print("\n[4/4] Testing comparison and recommendation...")
from agents.comparison_agent import compare_products
from agents.recommendation_agent import recommend_products
from app.graph import create_graph

comparisons = compare_products(products)
print(f"  - Compared {len(comparisons)} products")

recommendations = recommend_products(comparisons, top_n=3)
print(f"  - Generated {len(recommendations)} recommendations")

if recommendations:
    print("\nTop Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n  {i}. {rec['title']}")
        print(f"     Price: ${rec['price']}")
        print(f"     Rating: {rec['rating']}/5")
        print(f"     Justification: {rec['justification']}")

print("\nLangGraph pipeline test...")
graph = create_graph(db)
state = graph.invoke(
    {
        "query": "Laptop for gaming and programming under 1200",
        "preferences": None,
        "products": [],
        "comparisons": [],
        "recommendations": [],
        "errors": [],
        "used_fallback": False,
    }
)
print(f"  - Graph generated {len(state.get('recommendations', []))} recommendations")

print("\nAll tests completed successfully!")
db.close()
