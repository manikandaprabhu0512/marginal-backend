from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from db.crud import get_or_create_conversation
from db.models import User
from graph.ingestion_graph.ingestion_event_stream import ingestion_event_stream
from middleware.auth_middleware import verifyToken

router = APIRouter()

class FirstQueryRequest(BaseModel):
    query: str

@router.post("/conversations/{conversation_id}/first-query")
async def first_query(conversation_id: str, body: FirstQueryRequest, current_user: User = Depends(verifyToken)):
    await get_or_create_conversation(conversation_id, current_user.id)

    return StreamingResponse(
        ingestion_event_stream(conversation_id, body.query, current_user.id),
        media_type="text/event-stream",
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        }
    )
