from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

from db.database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import chat, conversation, ingest


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(ingest.router, tags=["ingestion"])
app.include_router(chat.router, tags=["chat"])
app.include_router(conversation.router, tags=["conversation"])