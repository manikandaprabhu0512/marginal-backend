from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

smaller_model = ChatOpenAI(model='gpt-5-nano-2025-08-07')
groq_model = ChatGroq(model="llama-3.3-70b-versatile")
larger_model = ChatOpenAI(model='gpt-5-mini-2025-08-07')
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=100)