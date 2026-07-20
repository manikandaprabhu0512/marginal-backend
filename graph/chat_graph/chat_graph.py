from langgraph.graph import END, START, StateGraph

from graph.chat_graph.chat_state import ChatState
from graph.chat_graph.nodes.add_sources_node import add_sources_node
from graph.chat_graph.nodes.confidence_node import confidence_node
from graph.chat_graph.nodes.context_analyzer_node import context_analyzer
from graph.chat_graph.nodes.create_notebook_node import create_notebook_node
from graph.chat_graph.nodes.general_knowledge_node import \
    general_knowledge_node
from graph.chat_graph.nodes.history_node import history_node
from graph.chat_graph.nodes.larger_model_node import larger_model_node
from graph.chat_graph.nodes.off_topic_decision_node import \
    off_topic_decision_node
from graph.chat_graph.nodes.query_understanding_node import \
    query_understanding_node
from graph.chat_graph.nodes.retrieve_context_node import retrieve_context_node
from graph.chat_graph.nodes.router import (route_after_confidence,
                                           route_after_off_topic_decision,
                                           route_after_query_understanding,
                                           route_after_smaller_model,
                                           router_after_context_analyzer)
from graph.chat_graph.nodes.save_assistant_node import save_assistant_node
from graph.chat_graph.nodes.save_user_node import save_user_node
from graph.chat_graph.nodes.smaller_model_node import smaller_model_node
from helper.checkpointer import checkpointer

builder = StateGraph(ChatState)

builder.add_node("history", history_node)
builder.add_node("save_user", save_user_node)
builder.add_node("query_understanding", query_understanding_node)
builder.add_node("off_topic_decision", off_topic_decision_node)
builder.add_node("add_sources", add_sources_node)
builder.add_node("create_notebook", create_notebook_node)
builder.add_node("retrieve_context", retrieve_context_node)
builder.add_node("context_analyzer", context_analyzer)
builder.add_node("general_knowledge", general_knowledge_node)
builder.add_node("smaller_model", smaller_model_node)
builder.add_node("confidence", confidence_node)
builder.add_node("larger_model", larger_model_node)
builder.add_node("save_assistant", save_assistant_node)

builder.add_edge(START, "history")
builder.add_edge("history", "query_understanding")

builder.add_conditional_edges(
    "query_understanding",
    route_after_query_understanding,
    {
        "retrieve_context": "retrieve_context",
        "save_user": "save_user",
        "off_topic_decision": "off_topic_decision",
    },
)

builder.add_conditional_edges(
    "off_topic_decision",
    route_after_off_topic_decision,
    {
        "general_knowledge": "general_knowledge",
        "add_sources": "add_sources",
        "create_notebook": "create_notebook", 
    },
)

builder.add_edge("add_sources", "retrieve_context")

builder.add_edge("retrieve_context", "context_analyzer")

builder.add_conditional_edges(
    "context_analyzer",
    router_after_context_analyzer,
    {
        "off_topic_decision" : "off_topic_decision",
        "smaller_model" : "smaller_model"
    }
)

builder.add_conditional_edges(
    "smaller_model",
    route_after_smaller_model,
    {
        "confidence": "confidence",
        "save_user": "save_user",
    },
)

builder.add_conditional_edges(
    "confidence",
    route_after_confidence,
    {
        "larger_model": "larger_model",
        "save_user": "save_user",
    },
)

builder.add_edge("general_knowledge", "save_user")
builder.add_edge("larger_model", "save_user")
builder.add_edge("save_user", "save_assistant")
builder.add_edge("create_notebook", END)
builder.add_edge("save_assistant", END)

chat_graph = builder.compile(
    checkpointer=checkpointer,
)