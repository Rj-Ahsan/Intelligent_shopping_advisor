from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models.product import Base
import os

# Database URL
DATABASE_URL = "sqlite:///./products.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
Base.metadata.create_all(bind=engine)