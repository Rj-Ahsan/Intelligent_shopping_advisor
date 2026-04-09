import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from models.product import Product
from sqlalchemy.orm import Session

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_vector_store(products):
    if not products:
        raise ValueError("No products to create vector store from")
    
    descriptions = [p.description or "" for p in products]
    embeddings = model.encode(descriptions)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.asarray(embeddings, dtype='float32'))
    return index, embeddings

def search_similar_products(query, index, products, embeddings, top_k=10):
    if not query or not index or not products:
        return []
    
    try:
        query_embedding = model.encode([query])
        distances, indices = index.search(np.asarray(query_embedding, dtype='float32'), min(top_k, len(products)))
        results = []
        for i in indices[0]:
            if i >= 0 and i < len(products):
                results.append(products[i])
        return results
    except Exception as e:
        print(f"Error in search_similar_products: {e}")
        return []