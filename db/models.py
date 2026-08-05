import os
from datetime import datetime, timedelta, timezone

import jwt
from beanie import Document, PydanticObjectId
from pwdlib import PasswordHash
from pydantic import Field
from pymongo import ASCENDING, DESCENDING, IndexModel

password_hash = PasswordHash.recommended()

class User(Document):
    name: str
    username: str
    email: str
    password: str
    remaining_tokens: int = 1000000
    number_of_conversations: int = 5
    refreshToken: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @staticmethod
    def get_password_hash(password: str) -> str:
        return password_hash.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> str:
        
        return password_hash.verify(plain_password, hashed_password)

    def generate_access_token(self) -> str:
        payload = {
            "_id": str(self.id),
            "username": self.username,
            "email": self.email,
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }

        secret = os.getenv("ACCESS_TOKEN_SECRET_KEY")
        algorithm = os.getenv("ALGORITHM", "HS256")

        if not secret:
            raise ValueError("ACCESS_TOKEN_SECRET_KEY is not set in environment variables")

        return jwt.encode(payload, secret, algorithm=algorithm)
    
    def generate_refresh_token(self) -> str:
        payload = {
            "_id": str(self.id),
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }

        secret = os.getenv("REFRESH_TOKEN_SECRET_KEY")
        algorithm = os.getenv("ALGORITHM", "HS256")

        if not secret:
            raise ValueError("REFRESH_TOKEN_SECRET_KEY is not set in environment variables")

        return jwt.encode(payload, secret, algorithm=algorithm)

    def generateRefreshToken(self) -> str:
            payload = {
                "_id": str(self.id),
                "username": self.username,
                "email": self.email
            }
            return jwt.encode(payload, os.getenv("ACCESS_TOKEN_SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    class Settings:
        name = "users"


class Conversation(Document):
    user_id: PydanticObjectId
    conversation_id: str
    title: str = "Untitled Notebook"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_count: int = 0
    max_source_count: int = 50

    class Settings:
        name = "conversations"
        indexes = [
            IndexModel(
                [("user_id", 1), ("conversation_id", 1)],
                unique=True
            ),
            IndexModel(
                [("user_id", ASCENDING), ("last_activity", DESCENDING)]
            )
        ]

class Turn(Document):
    conversation_id: str
    user: dict | None = None
    events: list[dict] | None = None
    assistant: dict | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "turns"


class Message(Document):
    conversation_id: str
    role: str
    content: str
    file_url: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "messages"


class Source(Document):
    conversation_id: str
    url: str
    title: str
    source_type: str = "link"   # "link" | "pdf" | "text" | "document" | "video"
    vector_ids: list[str] = Field(default_factory=list)

    class Settings:
        name = "sources"

class ScrapedURLs(Document):
    conversation_id: str
    query: str
    url_list: list[dict] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "scraped_urls"
        indexes = [
            [("conversation_id", 1), ("query", 1)]
        ]
