import os

from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME", "notebooklm")

client = MongoClient(MONGODB_URI)

checkpointer = MongoDBSaver(
    client=client,
    db_name=DB_NAME,
)