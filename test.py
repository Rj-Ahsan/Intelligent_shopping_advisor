from app.graph import create_graph
from database.connection import SessionLocal
from utils.data_loader import load_products_to_db
from utils.vector_store import create_vector_store
from models.product import Product

db = SessionLocal()
load_products_to_db(db)
products = db.query(Product).all()
index, _ = create_vector_store(products)
graph = create_graph(db, index, products)

result = graph.invoke({"query": "Best smartphone under 100"})
print(result["recommendations"])