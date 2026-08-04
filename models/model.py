from langchain_litellm import ChatLiteLLM
from langchain_openai import OpenAIEmbeddings

# ====================== [ Smaller Model with fallback ] ========================================

smaller_model_primary = ChatLiteLLM(model='gpt-5-nano-2025-08-07')
smaller_model_fallback_1 = ChatLiteLLM(model='groq/llama-3.3-70b-versatile')
smaller_model_fallback_2 = ChatLiteLLM(model='gemini-1.5-flash-lite')

smaller_model = smaller_model_primary.with_fallbacks([smaller_model_fallback_1, smaller_model_fallback_2])

# ====================== [ groq Model with fallback ] ========================================

groq_model_primary = ChatLiteLLM(model='groq/openai/gpt-oss-20b')
groq_model_fallback_1 = ChatLiteLLM(model='gpt-4o-mini')
groq_model_fallback_2 = ChatLiteLLM(model='gemini-1.5-flash-lite')

groq_model = groq_model_primary.with_fallbacks([groq_model_fallback_1, groq_model_fallback_2])

# ====================== [ Larger Model with fallback ] ========================================

larger_model_primary = ChatLiteLLM(model='gpt-5-mini-2025-08-07')
larger_model_fallback_1 = ChatLiteLLM(model='groq/llama-3.3-70b-versatile')
larger_model_fallback_2 = ChatLiteLLM(model='gemini-1.5-flash-lite')


larger_model = larger_model_primary.with_fallbacks([larger_model_fallback_1, larger_model_fallback_2])

# ====================== [ Embedding Model ] ========================================

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=100)