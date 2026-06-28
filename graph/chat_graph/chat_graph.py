from langgraph.graph import END, START, StateGraph

from graph.chat_graph.chat_state import ChatState
from graph.chat_graph.nodes.confidence_node import confidence_node
from graph.chat_graph.nodes.history_node import history_node
from graph.chat_graph.nodes.larger_model_node import larger_model_node
from graph.chat_graph.nodes.retrieve_context_node import retrieve_context_node
from graph.chat_graph.nodes.router import (route_after_confidence,
                                           route_after_smaller_model)
from graph.chat_graph.nodes.save_assistant_node import save_assistant_node
from graph.chat_graph.nodes.save_user_node import save_user_node
from graph.chat_graph.nodes.smaller_model_node import smaller_model_node

builder = StateGraph(ChatState)

builder.add_node("history", history_node)
builder.add_node("save_user", save_user_node)
builder.add_node("retrieve_context", retrieve_context_node)
builder.add_node("smaller_model", smaller_model_node)
builder.add_node("confidence", confidence_node)
builder.add_node("larger_model", larger_model_node)
builder.add_node("save_assistant", save_assistant_node)

builder.add_edge(START, "history")
builder.add_edge("history", "save_user")
builder.add_edge("save_user", "retrieve_context")
builder.add_edge("retrieve_context", "smaller_model")

builder.add_conditional_edges(
    "smaller_model",
    route_after_smaller_model,
    {
        "confidence": "confidence",
        "save_assistant": "save_assistant",
    },
)

builder.add_conditional_edges(
    "confidence",
    route_after_confidence,
    {
        "larger_model": "larger_model",
        "save_assistant": "save_assistant",
    },
)

builder.add_edge("larger_model", "save_assistant")
builder.add_edge("save_assistant", END)

chat_graph = builder.compile()