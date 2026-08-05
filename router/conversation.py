from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from db.crud import (db_get_conversation, delete_source_db,
                     get_or_create_conversation, get_source, get_sources,
                     get_turns, list_conversations, save_sources,
                     update_conversation_title)
from db.models import User
from middleware.auth_middleware import verifyToken

router = APIRouter()

class TitleRequest(BaseModel):
    title: str

class SourceRequest(BaseModel):
    src : list[dict]

class CreateConversationRequest(BaseModel):
    conversation_id : str
    title: str = "Untitled Notebook"

@router.get("/conversations")
async def get_conversation(current_user: User = Depends(verifyToken)):
    return await list_conversations(current_user.id)

@router.post("/conversations", status_code=status.HTTP_201_CREATED)
async def create_notebook(body: CreateConversationRequest, current_user: User = Depends(verifyToken)):
    conv = await get_or_create_conversation(body.conversation_id, current_user.id, body.title)
    return {
        "conversation_id": conv.conversation_id,
        "title": conv.title,
    }

@router.get("/conversations/{conversation_id}")
async def get_notebook(conversation_id: str, current_user: User = Depends(verifyToken)):
    conv = await db_get_conversation(conversation_id, current_user.id)
    if not conv:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return conv

@router.get("/conversations/{conversation_id}/turns", status_code=status.HTTP_200_OK)
async def get_conversation_turns(conversation_id: str, _: User = Depends(verifyToken)):
    return await get_turns(conversation_id)

@router.patch("/conversations/{conversation_id}/title", status_code=status.HTTP_200_OK)
async def update_title(conversation_id: str, body: TitleRequest, current_user: User = Depends(verifyToken)):
    return await update_conversation_title(conversation_id, current_user.id, body.title)

@router.get("/conversations/{conversation_id}/sources")
async def get_conversation_sources(conversation_id: str, _: User = Depends(verifyToken)):
    return await get_sources(conversation_id)

@router.get("/conversations/sources/{source_id}")
async def get_conversation_source(source_id: PydanticObjectId, _: User = Depends(verifyToken)):
    return await get_source(source_id)

@router.post("/conversations/{conversation_id}/add-sources")
async def add_sources(conversation_id: str, body: SourceRequest, _: User = Depends(verifyToken)):
    return await save_sources(conversation_id, body.sources)

@router.delete("/conversations/{conversation_id}/sources/{source_id}")
async def delete_source(conversation_id: str, source_id: PydanticObjectId, _: User = Depends(verifyToken)):
    return await delete_source_db(conversation_id, source_id) 

# @router.delete("/conversations/{conversation_id}")
# async def delete_conversation(conversation_id: str):
#     return await