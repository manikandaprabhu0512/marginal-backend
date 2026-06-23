from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from helper.process_chat import process_chat

router = APIRouter()

@router.post("/conversations/{conversation_id}/message")
async def send_message(
    conversation_id: str,
    message: str = Form(default=""),
    files: list[UploadFile] = File(default=[]),
    excluded_urls: str = Form(default="[]"),
):
    return StreamingResponse(
        process_chat(conversation_id, message, files, excluded_urls),
        media_type="text/event-stream",
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        }
    )