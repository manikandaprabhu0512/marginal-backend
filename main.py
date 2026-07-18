from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config.cloudinary_config
import telemetry.instrumentation
from db.database import init_db
from router import chat, conversation, ingest
from telemetry.instrumentation import tracer


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://marginal-frontend-iota.vercel.app"
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