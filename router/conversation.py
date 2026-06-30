from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.crud import (db_get_conversation, delete_source_db, get_messages,
                     get_or_create_conversation, get_source, get_sources,
                     list_conversations, save_sources,
                     update_conversation_title)
from db.models import Conversation

router = APIRouter()

class TitleRequest(BaseModel):
    title: str

class SourceRequest(BaseModel):
    src : list[dict]

@router.get("/health")
async def get_health():
    return {"status": "ok"}

@router.get("/conversations")
async def get_conversation():
    return await list_conversations()

@router.post("/conversations")
async def create_notebook(body: Conversation):
    conv = await get_or_create_conversation(body.conversation_id, body.title)
    return {
        "conversation_id": conv.conversation_id,
        "title": conv.title,
    }

@router.get("/conversations/{conversation_id}")
async def get_notebook(conversation_id: str):
    conv = await db_get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return conv

@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: str):
    return await get_messages(conversation_id)

@router.patch("/conversations/{conversation_id}/title")
async def update_title(conversation_id: str, body: TitleRequest):
    return await update_conversation_title(conversation_id, body.title)

@router.get("/conversations/{conversation_id}/sources")
async def get_conversation_sources(conversation_id: str):
    return await get_sources(conversation_id)

@router.get("/conversations/sources/{source_id}")
async def get_conversation_source(source_id: PydanticObjectId):
    return await get_source(source_id)

@router.post("/conversations/{conversation_id}/add-sources")
async def add_sources(conversation_id: str, body: SourceRequest):
    return await save_sources(conversation_id, body.sources)

@router.delete("/conversations/{conversation_id}/sources/{source_id}")
async def delete_source(conversation_id: str, source_id: PydanticObjectId):
    return await delete_source_db(conversation_id, source_id) 

# @router.delete("/conversations/{conversation_id}")
# async def delete_conversation(conversation_id: str):
#     return await