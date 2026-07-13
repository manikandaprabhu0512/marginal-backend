from langchain.tools import tool

from config.pincone_config import get_vector_store
from telemetry.instrumentation import tracer


async def retrieve_context(conversation_id: str, query: str, excluded_urls: list[str] = None) -> str:
    """Direct Python call — retrieves context from Pinecone."""

    with tracer.start_as_current_span("Vector Store"):
        vector_store = get_vector_store(conversation_id)

    filter_dict = {"url": {"$nin": excluded_urls}} if excluded_urls else None

    with tracer.start_as_current_span("Similarity Search"):
        docs = await vector_store.asimilarity_search(query=query, k=4, filter=filter_dict)

    return "\n\n".join(doc.page_content for doc in docs)


# def make_retriever_tool(conversation_id: str):
#     vector_store = get_vector_store(conversation_id)

#     @tool
#     async def retriever_tool(query: str, excluded_urls: list[str] = None):
#         """Retrieve relevant content from this conversation's knowledge base."""
#         filter_dict = {"url": {"$nin": excluded_urls}} if excluded_urls else None
#         docs = await vector_store.asimilarity_search(query=query, k=4, filter=filter_dict)
#         return "\n\n".join(doc.page_content for doc in docs)

#     return retriever_tool