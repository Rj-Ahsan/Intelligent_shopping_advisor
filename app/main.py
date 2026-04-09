from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.connection import get_db
from pydantic import BaseModel, ConfigDict
from models.product import Product
from typing import List, Optional, Any
from app.graph import create_graph
from database.connection import SessionLocal
from utils.data_loader import load_products_to_db
from utils.vector_store import create_vector_store

APP_STATE: dict[str, Any] = {"index": None, "products": []}


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        load_products_to_db(db)
        products = db.query(Product).all()
        APP_STATE["products"] = products
        if products:
            index, _ = create_vector_store(products)
            APP_STATE["index"] = index
        yield
    finally:
        db.close()


app = FastAPI(title="Product Recommendation API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    price: float
    description: str
    rating_rate: float = 0.0
    justification: Optional[str] = None

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running"}

@app.get("/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """Get all products"""
    try:
        products = db.query(Product).offset(skip).limit(limit).all()
        return products
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []

@app.post("/recommend", response_model=List[ProductResponse])
def get_recommendations(request: QueryRequest, db: Session = Depends(get_db)):
    """Get top 3-5 recommendations using LangGraph multi-agent pipeline."""
    try:
        graph = create_graph(db, APP_STATE.get("index"), APP_STATE.get("products"))
        final_state = graph.invoke(
            {
                "query": request.query,
                "preferences": None,
                "products": [],
                "comparisons": [],
                "recommendations": [],
                "errors": [],
                "used_fallback": False,
            }
        )

        recommendations = final_state.get("recommendations", [])[:5]
        if recommendations:
            return [
                ProductResponse(
                    id=idx + 1,
                    title=item["title"],
                    price=item["price"],
                    description=item["description"],
                    rating_rate=item.get("rating", 0.0),
                    justification=item.get("justification"),
                )
                for idx, item in enumerate(recommendations)
            ]

        # Hard fallback when graph returns nothing
        fallback_products = db.query(Product).order_by(Product.rating_rate.desc()).limit(5).all()
        return [
            ProductResponse(
                id=p.id,
                title=p.title,
                price=p.price,
                description=p.description,
                rating_rate=p.rating_rate or 0.0,
                justification="Fallback recommendation based on top-rated available products.",
            )
            for p in fallback_products
        ]
    except Exception as e:
        print(f"Error in recommendations: {e}")
        return []

@app.get("/products/search")
def search_products(query: str, db: Session = Depends(get_db)):
    """Search products by title or category"""
    try:
        search_term = query.lower()
        products = db.query(Product).filter(
            (Product.title.ilike(f"%{search_term}%")) | 
            (Product.category.ilike(f"%{search_term}%"))
        ).limit(10).all()
        return products
    except Exception as e:
        print(f"Error in search: {e}")
        return []