from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Any, Optional
from agents.preference_agent import extract_preferences, Preferences
from agents.product_retrieval_agent import retrieve_products
from agents.comparison_agent import compare_products
from agents.recommendation_agent import recommend_products
from sqlalchemy.orm import Session

class State(TypedDict):
    query: str
    preferences: Preferences
    products: List[Any]
    comparisons: List[dict]
    recommendations: List[dict]
    errors: List[str]
    used_fallback: bool

def preference_node(state: State):
    try:
        state["preferences"] = extract_preferences(state.get("query", ""))
    except Exception as e:
        print(f"Error in preference_node: {e}")
        state["preferences"] = Preferences()
        state.setdefault("errors", []).append("preference_node_failed")
    return state

def retrieval_node(state: State, db: Session, index: Optional[Any] = None, products: Optional[List[Any]] = None):
    try:
        state["products"] = retrieve_products(state.get("preferences", Preferences()), db, index, products)
    except Exception as e:
        print(f"Error in retrieval_node: {e}")
        state["products"] = []
        state.setdefault("errors", []).append("retrieval_node_failed")
    return state


def fallback_retrieval_node(state: State, db: Session):
    # Fallback path: if semantic/category retrieval returns no products,
    # try broader retrieval while still respecting budget when available.
    try:
        preferences = state.get("preferences", Preferences())
        from models.product import Product
        all_products = db.query(Product).all()

        if preferences.budget is not None:
            all_products = [p for p in all_products if p.price <= preferences.budget]

        state["products"] = all_products[:20]
        state["used_fallback"] = True
    except Exception as e:
        print(f"Error in fallback_retrieval_node: {e}")
        state["products"] = []
        state.setdefault("errors", []).append("fallback_retrieval_failed")
    return state

def comparison_node(state: State):
    try:
        products = state.get("products", [])
        if products:
            state["comparisons"] = compare_products(products)
        else:
            state["comparisons"] = []
    except Exception as e:
        print(f"Error in comparison_node: {e}")
        state["comparisons"] = []
        state.setdefault("errors", []).append("comparison_node_failed")
    return state

def recommendation_node(state: State):
    try:
        comparisons = state.get("comparisons", [])
        if comparisons:
            state["recommendations"] = recommend_products(comparisons)
        else:
            state["recommendations"] = []
    except Exception as e:
        print(f"Error in recommendation_node: {e}")
        state["recommendations"] = []
        state.setdefault("errors", []).append("recommendation_node_failed")
    return state


def route_after_retrieval(state: State) -> str:
    products = state.get("products", [])
    return "fallback_retrieval" if not products else "comparison"


def route_after_fallback(state: State) -> str:
    products = state.get("products", [])
    return "comparison" if products else END

def create_graph(db: Session, index=None, products=None):
    try:
        graph = StateGraph(State)
        graph.add_node("preference", preference_node)
        graph.add_node("retrieval", lambda s: retrieval_node(s, db, index, products))
        graph.add_node("fallback_retrieval", lambda s: fallback_retrieval_node(s, db))
        graph.add_node("comparison", comparison_node)
        graph.add_node("recommendation", recommendation_node)
        
        graph.add_edge("preference", "retrieval")
        graph.add_conditional_edges(
            "retrieval",
            route_after_retrieval,
            {"fallback_retrieval": "fallback_retrieval", "comparison": "comparison"},
        )
        graph.add_conditional_edges(
            "fallback_retrieval",
            route_after_fallback,
            {"comparison": "comparison", END: END},
        )
        graph.add_edge("comparison", "recommendation")
        graph.add_edge("recommendation", END)
        
        graph.set_entry_point("preference")
        return graph.compile()
    except Exception as e:
        print(f"Error creating graph: {e}")
        # Return a simple function-based graph as fallback
        def simple_graph(state):
            state = preference_node(state)
            state = retrieval_node(state, db, index, products)
            if not state.get("products"):
                state = fallback_retrieval_node(state, db)
            state = comparison_node(state)
            state = recommendation_node(state)
            return state
        return simple_graph