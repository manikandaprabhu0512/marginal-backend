import asyncio
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

from config.pincone_config import get_vector_store
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=100)

executor = ThreadPoolExecutor(max_workers=10)

async def vectorize_page(conversation_id: str, url: str, title: str, content: str):
    vector_store = get_vector_store(conversation_id)

    docs = [Document(page_content=content, metadata={"url": url, "title": title, "stored_at": time.time()})]
    splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    vector_ids = [f"{hashlib.md5(url.encode()).hexdigest()}-{i}" for i in range(len(split_docs))]

    t2 = time.time()
    await vector_store.aadd_documents(documents=split_docs, ids=vector_ids, batch_size=100, embedding_chunk_size=1000)
    print(f"Pinecone Upsert {url}: {time.time()-t2:.2f}s")

    return vector_ids

async def delete_vectorize(conversation_id: str, vector_ids: list[str]):
    vector_store = get_vector_store(conversation_id)
    await vector_store.adelete(ids=vector_ids)