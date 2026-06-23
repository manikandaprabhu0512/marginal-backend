import os

from beanie import init_beanie
from db.models import Conversation, Message, Source
from pymongo import AsyncMongoClient

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME", "notebooklm")


async def init_db():
    client = AsyncMongoClient(MONGODB_URI)
    await init_beanie(
        database=client[DB_NAME],
        document_models=[Conversation, Message, Source],
    )