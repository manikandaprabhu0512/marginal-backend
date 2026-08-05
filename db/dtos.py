from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id : PydanticObjectId
    name: str
    username: str
    email: str
    remaining_tokens: int
    number_of_conversations: int
    created_at: datetime
    last_activity: datetime

class LoginRequest(BaseModel):
    username: str | None = None
    password: str
    email: str | None = None