import hashlib
import os

from langchain_pinecone import PineconeVectorStore
from models.model import embeddings
from pinecone import Pinecone, ServerlessSpec

INDEX_NAME = "main-index"

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

if not pc.has_index(INDEX_NAME):
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

_index = pc.Index(INDEX_NAME, pool_threads = 30)

# def get_namespace(conversation_id: str) -> str:
#     """Derive a fixed-length, valid namespace from conversation_id."""
#     return hashlib.sha256(conversation_id.encode()).hexdigest()

def get_vector_store(conversation_id: str) -> PineconeVectorStore:
    return PineconeVectorStore(
        index=_index,
        embedding=embeddings,
        namespace=conversation_id,
    )