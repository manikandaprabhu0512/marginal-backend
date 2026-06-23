from db.crud import get_or_create_conversation
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from flows.ingestion import run_ingestion_stream
from pydantic import BaseModel

router = APIRouter()


class FirstQueryRequest(BaseModel):
    query: str

@router.post("/conversations/{conversation_id}/first-query")
async def first_query(conversation_id: str, body: FirstQueryRequest):
    await get_or_create_conversation(conversation_id)

    return StreamingResponse(
        run_ingestion_stream(conversation_id, body.query),
        media_type="text/event-stream",
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        }
    )
    # ingestion_result = await run_ingestion(conversation_id, body.query)
    # chat_result = await run_chat(conversation_id, body.query)

    # return {
    #     "title": ingestion_result["title"],
    #     "answer": chat_result["assistant"].content,
    #     "stats": {
    #         "urls_found": ingestion_result["urls_found"],
    #         "urls_stored": ingestion_result["urls_stored"],
    #         "sources": ingestion_result["sources"]
    #     },
    #     "confidence": chat_result.get("confidence"),
    # }

