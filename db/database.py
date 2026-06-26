import os

from beanie import init_beanie
from pymongo import AsyncMongoClient

from db.models import Conversation, Message, ScrapedURLs, Source

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME", "notebooklm")


async def init_db():
    client = AsyncMongoClient(MONGODB_URI)
    await init_beanie(
        database=client[DB_NAME],
        document_models=[Conversation, Message, Source, ScrapedURLs],
    )