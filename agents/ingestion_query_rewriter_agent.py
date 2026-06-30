# agents/ingestion_query_rewriter.py
from langchain.agents import create_agent

from models.model import groq_model
from prompts import load_prompt

_ingestion_query_rewriter = create_agent(
    groq_model,
    [],
    system_prompt=load_prompt("ingestion_query_rewriter_prompt"),
    name="ingestion_query_rewriter"
)

def get_ingestion_query_rewriter():
    return _ingestion_query_rewriter