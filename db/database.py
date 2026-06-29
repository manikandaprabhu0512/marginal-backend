import os

from beanie import init_beanie
from pymongo import AsyncMongoClient

from db.models import Conversation, Message, ScrapedURLs, Source

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME", "notebooklm")

client = AsyncMongoClient(MONGODB_URI)

async def init_db():
    await init_beanie(
        database=client[DB_NAME],
        document_models=[Conversation, Message, Source, ScrapedURLs],
    )