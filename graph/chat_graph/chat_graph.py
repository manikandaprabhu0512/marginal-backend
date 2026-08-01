from langgraph.graph import END, START, StateGraph

from graph.chat_graph.chat_state import ChatState
from graph.chat_graph.nodes.add_sources_node import add_sources_node
from graph.chat_graph.nodes.confidence_node import confidence_node
from graph.chat_graph.nodes.context_analyzer_node import context_analyzer
from graph.chat_graph.nodes.context_conformation_node import \
    context_conformation_node
from graph.chat_graph.nodes.create_notebook_node import create_notebook_node
from graph.chat_graph.nodes.general_knowledge_node import \
    general_knowledge_node
from graph.chat_graph.nodes.history_node import history_node
from graph.chat_graph.nodes.intent_classifier_node import \
    intent_classifier_node
from graph.chat_graph.nodes.larger_model_node import larger_model_node
from graph.chat_graph.nodes.off_topic_decision_node import \
    off_topic_decision_node
from graph.chat_graph.nodes.query_rewritter_agent_node import \
    query_rewritter_node
from graph.chat_graph.nodes.retrieve_context_node import retrieve_context_node
from graph.chat_graph.nodes.router import (route_after_confidence,
                                           route_after_off_topic_decision,
                                           route_after_query_rewritter,
                                           route_after_smaller_model,
                                           router_after_context_analyzer)
from graph.chat_graph.nodes.save_conversation_node import \
    save_conversation_node
from graph.chat_graph.nodes.smaller_model_node import smaller_model_node
from helper.checkpointer import checkpointer

builder = StateGraph(ChatState)

builder.add_node("history", history_node)
builder.add_node("intent_classifier", intent_classifier_node)
builder.add_node("query_rewritter", query_rewritter_node)
builder.add_node("off_topic_decision", off_topic_decision_node)
builder.add_node("add_sources", add_sources_node)
builder.add_node("create_notebook", create_notebook_node)
builder.add_node("retrieve_context", retrieve_context_node)
builder.add_node("context_analyzer", context_analyzer)
builder.add_node("context_confirmation", context_conformation_node)
builder.add_node("general_knowledge", general_knowledge_node)
builder.add_node("smaller_model", smaller_model_node)
builder.add_node("confidence", confidence_node)
builder.add_node("larger_model", larger_model_node)
builder.add_node("save_conversation", save_conversation_node)

builder.add_edge(START, "history")
builder.add_edge("history", "intent_classifier")

builder.add_conditional_edges(
    "intent_classifier",
    route_after_query_rewritter,
    {
        "save_conversation": "save_conversation",
        "query_rewritter": "query_rewritter",
    }
)

builder.add_edge("query_rewritter", "retrieve_context")
builder.add_edge("retrieve_context", "context_analyzer")

builder.add_conditional_edges(
    "context_analyzer",
    router_after_context_analyzer,
    {
        "off_topic_decision" : "off_topic_decision",
        "context_confirmation" : "context_confirmation",
    }
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

builder.add_edge("context_confirmation", "smaller_model")

builder.add_edge("add_sources", "retrieve_context")

builder.add_conditional_edges(
    "smaller_model",
    route_after_smaller_model,
    {
        "confidence": "confidence",
        "save_conversation": "save_conversation",
    },
)

builder.add_conditional_edges(
    "confidence",
    route_after_confidence,
    {
        "larger_model": "larger_model",
        "save_conversation": "save_conversation",
    },
)

builder.add_edge("general_knowledge", "save_conversation")
builder.add_edge("larger_model", "save_conversation")
builder.add_edge("create_notebook", END)
builder.add_edge("save_conversation", END)

chat_graph = builder.compile(
    checkpointer=checkpointer,
)