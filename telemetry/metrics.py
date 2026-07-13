from telemetry.instrumentation import meter

# ==========================================================
# Counters
# ==========================================================

chat_requests = meter.create_counter(
    name="chat.requests",
    description="Total chat requests",
)

chat_completed = meter.create_counter(
    name="chat.completed",
    description="Total completed chat requests",
)

chat_failed = meter.create_counter(
    name="chat.failed",
    description="Total failed chat requests",
)

llm_calls = meter.create_counter(
    name="llm.calls",
    description="Total LLM calls",
)

groq_llm_calls = meter.create_counter(
    name="groq.llm.calls",
    description="Total Groq LLM calls",
)

openai_llm_calls = meter.create_counter(
    name="openai.llm.calls",
    description="Total OpenAI LLM calls",
)

retriever_calls = meter.create_counter(
    name="retriever.calls",
    description="Total retriever calls",
)

off_topic_requests = meter.create_counter(
    name="offtopic.requests",
    description="Total off-topic requests",
)

continue_general = meter.create_counter(
    name="hitl.continue_general",
    description="User selected Continue General",
)

add_sources = meter.create_counter(
    name="hitl.add_sources",
    description="User selected Add Sources",
)

create_notebook = meter.create_counter(
    name="hitl.create_notebook",
    description="User selected Create Notebook",
)

urls_processed = meter.create_counter(
    name="ingestion.urls_processed",
    description="Total processed URLs",
)


# ==========================================================
# Histograms
# ==========================================================

chat_duration = meter.create_histogram(
    name="chat.duration",
    unit="s",
    description="Chat request duration",
)

llm_duration = meter.create_histogram(
    name="llm.duration",
    unit="s",
    description="LLM execution duration",
)

retriever_duration = meter.create_histogram(
    name="retriever.duration",
    unit="s",
    description="Retriever execution duration",
)

similarity_search_duration = meter.create_histogram(
    name="retriever.similarity_search.duration",
    unit="s",
    description="Similarity search duration",
)

embedding_duration = meter.create_histogram(
    name="embedding.duration",
    unit="s",
    description="Embedding generation duration",
)

confidence_duration = meter.create_histogram(
    name="confidence.duration",
    unit="s",
    description="Confidence evaluation duration",
)

ingestion_duration = meter.create_histogram(
    name="ingestion.duration",
    unit="s",
    description="Notebook ingestion duration",
)

url_processing_duration = meter.create_histogram(
    name="ingestion.url_processing.duration",
    unit="s",
    description="Single URL processing duration",
)