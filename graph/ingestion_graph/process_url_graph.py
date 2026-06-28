from langgraph.graph import END, START, StateGraph

from graph.ingestion_graph.nodes.load_page_node import load_page_node
from graph.ingestion_graph.nodes.page_vectorizer_node import \
    page_vectorizer_node
from graph.ingestion_graph.nodes.save_source_node import save_source_node
from graph.ingestion_graph.worker_state import WorkerState

builder = StateGraph(WorkerState)

builder.add_node("load_page", load_page_node)
builder.add_node("vectorize", page_vectorizer_node)
builder.add_node("save_source", save_source_node)

builder.add_edge(START, "load_page")
builder.add_edge("load_page", "vectorize")
builder.add_edge("vectorize", "save_source")
builder.add_edge("save_source", END)

process_url_graph = builder.compile()