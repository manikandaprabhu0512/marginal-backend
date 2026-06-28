from langgraph.graph import END, START, StateGraph

from graph.ingestion_graph.nodes.process_urls_node import process_urls_node
from graph.ingestion_graph.nodes.scrape_urls_node import search_node
from graph.ingestion_graph.nodes.title_node import title_node
from graph.ingestion_graph.state import GraphState

builder = StateGraph(GraphState)

builder.add_node("title", title_node)
builder.add_node("search", search_node)
builder.add_node("process_urls", process_urls_node)

builder.add_edge(START, "title")
builder.add_edge("title", "search")
builder.add_edge("search", "process_urls")
builder.add_edge("process_urls", END)

graph = builder.compile()