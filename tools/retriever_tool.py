from langchain.tools import tool

from config.pincone_config import get_vector_store


async def retrieve_context(conversation_id: str, query: str, excluded_urls: list[str] = None) -> str:
    """Direct Python call — retrieves context from Pinecone."""
    vector_store = get_vector_store(conversation_id)
    filter_dict = {"url": {"$nin": excluded_urls}} if excluded_urls else None
    print(filter_dict)
    docs = await vector_store.asimilarity_search(query=query, k=4, filter=filter_dict)
    print("doc: ", docs)
    return "\n\n".join(doc.page_content for doc in docs)


def make_retriever_tool(conversation_id: str):
    vector_store = get_vector_store(conversation_id)

    @tool
    async def retriever_tool(query: str, excluded_urls: list[str] = None):
        """Retrieve relevant content from this conversation's knowledge base."""
        print("Retervial Tool called...")
        filter_dict = {"url": {"$nin": excluded_urls}} if excluded_urls else None
        print(filter_dict)
        docs = await vector_store.asimilarity_search(query=query, k=4, filter=filter_dict)
        print("doc: ", docs)
        return "\n\n".join(doc.page_content for doc in docs)

    return retriever_tool