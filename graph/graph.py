from langgraph.graph import END, START, StateGraph

from graph.nodes.load_page_node import load_page_node
from graph.nodes.page_vectorizer import page_vectorizer_node
from graph.nodes.save_source_node import save_source_node
from graph.nodes.scrape_urls_node import search_node
from graph.nodes.title_node import title_node
from graph.state import GraphState

builder = StateGraph(GraphState)

print("Building graph...")

builder.add_node("title", title_node)
builder.add_node("search", search_node)
builder.add_node("load_page", load_page_node)
builder.add_node("page_vectorizer", page_vectorizer_node)
builder.add_node("save_source", save_source_node)

builder.add_edge(START, "title")
builder.add_edge("title", "search")
builder.add_edge("search", "load_page")
builder.add_edge("load_page", "page_vectorizer")
builder.add_edge("page_vectorizer", "save_source")
builder.add_edge("save_source", END)

graph = builder.compile()