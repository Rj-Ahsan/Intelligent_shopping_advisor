import time
from statistics import mean
from app.graph import create_graph
from database.connection import SessionLocal
from models.product import Product
from utils.data_loader import load_products_to_db
from utils.vector_store import create_vector_store


TEST_QUERIES = [
    "Best smartphone under 1000",
    "Best smartphone under 500",
    "Best smartphone under 300",
    "Affordable phone with battery life",
    "Laptop for gaming and programming",
    "Laptop for office work under 1200",
    "Electronics under 200",
    "Top electronics for students",
    "Good camera phone below 800",
    "Performance laptop under 1500",
    "Jewelry under 300",
    "Ring for gift",
    "Necklace under 250",
    "Women's fashion budget 100",
    "Men jacket under 200",
    "Best rated products",
    "Cheap products",
    "Value for money electronics",
    "Programming laptop with performance",
    "Battery phone for travel",
    "Mobile for casual usage",
    "Gaming setup product",
    "Office laptop lightweight",
    "Durable smartphone",
    "Camera focused mobile",
    "Student laptop below 900",
    "Premium jewelry set",
    "bracelet under 200",
    "women dress casual",
    "men clothing office",
    "product under 50",
    "electronics under 100",
    "electronics under 10000",
    "best product under pkr 100000",
    "phone below pkr 70000",
    "laptop under rs 200000",
    "I want something good but cheap",
    "recommend me any product",
    "Need a gift for sister",
    "Need a gift for brother",
    "smartphone",
    "laptop",
    "jewelry",
    "clothes",
    "student budget item",
    "high performance item",
    "gaming item under 400",
    "conflicting query expensive and cheap",
    "no budget no category",
    "under 10",
]


def evaluate():
    db = SessionLocal()
    try:
        load_products_to_db(db)
        products = db.query(Product).all()
        index, _ = create_vector_store(products)
        graph = create_graph(db, index, products)

        response_times = []
        non_empty_recommendations = 0

        for query in TEST_QUERIES:
            start = time.perf_counter()
            state = graph.invoke(
                {
                    "query": query,
                    "preferences": None,
                    "products": [],
                    "comparisons": [],
                    "recommendations": [],
                    "errors": [],
                    "used_fallback": False,
                }
            )
            elapsed_ms = (time.perf_counter() - start) * 1000
            response_times.append(elapsed_ms)
            if state.get("recommendations"):
                non_empty_recommendations += 1

        relevance_rate = (non_empty_recommendations / len(TEST_QUERIES)) * 100
        print("=== Evaluation Results (50 Queries) ===")
        print(f"Queries tested: {len(TEST_QUERIES)}")
        print(f"Non-empty recommendations: {non_empty_recommendations}")
        print(f"Recommendation relevance rate: {relevance_rate:.2f}%")
        print(f"Avg response time: {mean(response_times):.2f} ms")
        print(f"Min response time: {min(response_times):.2f} ms")
        print(f"Max response time: {max(response_times):.2f} ms")
    finally:
        db.close()


if __name__ == "__main__":
    evaluate()
