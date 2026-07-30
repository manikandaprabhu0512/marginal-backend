import hashlib
import time

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.pincone_config import _index, get_vector_store
from models.model import embedding_model


async def vectorize_page(
    conversation_id: str,
    url: str,
    title: str,
    content: str,
):
    # vector_store = get_vector_store(conversation_id)

    docs = [
        Document(
            page_content=content,
            metadata={
                "url": url,
                "title": title,
                "stored_at": time.time(),
            },
        )
    ]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200,
    )

    # -----------------------------
    # Split
    # -----------------------------
    start = time.perf_counter()

    split_docs = splitter.split_documents(docs)

    print(f"Split Time: {time.perf_counter() - start:.2f}s")
    print(f"Content Length: {len(content)}")
    print(f"Chunks: {len(split_docs)}")

    vector_ids = [
        f"{hashlib.md5(url.encode()).hexdigest()}-{i}"
        for i in range(len(split_docs))
    ]
    print("Vector IDs Generated...")

    texts = [doc.page_content for doc in split_docs]
    print("Texts Extracted...")

    # ==========================================================
    # STEP 1 : EMBEDDING
    # ==========================================================

    print("Embedding Model Loaded...")

    start = time.perf_counter()

    embeddings = await embedding_model.aembed_documents(texts)
    print("Text Embedded...")

    embedding_time = time.perf_counter() - start

    print(f"Embedding Time: {embedding_time:.2f}s")

    # ==========================================================
    # STEP 2 : PREPARE VECTORS
    # ==========================================================

    start = time.perf_counter()

    vectors = [
        {
            "id": vector_id,
            "values": embedding,
            "metadata": {
                **doc.metadata,
                "text": doc.page_content,
            },
        }
        for vector_id, embedding, doc in zip(
            vector_ids,
            embeddings,
            split_docs,
        )
    ]

    print(f"Vector Build Time: {time.perf_counter() - start:.2f}s")

    # ==========================================================
    # STEP 3 : UPSERT
    # ==========================================================

    start = time.perf_counter()

    _index.upsert(
        vectors=vectors,
        namespace=conversation_id,
    )

    upsert_time = time.perf_counter() - start

    print(f"Upsert Time: {upsert_time:.2f}s")

    print("=" * 50)
    print(f"Embedding : {embedding_time:.2f}s")
    print(f"Upsert    : {upsert_time:.2f}s")
    print(f"Total     : {embedding_time + upsert_time:.2f}s")
    print("=" * 50)

    return vector_ids

async def delete_vectorize(conversation_id: str, vector_ids: list[str]):
    vector_store = get_vector_store(conversation_id)
    await vector_store.adelete(ids=vector_ids)