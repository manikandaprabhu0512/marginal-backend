from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from graph.chat_graph.chat_event_resume_stream import chat_event_resume_stream
from helper.process_chat import process_chat


class ResumeRequest(BaseModel):
    decision: str

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

@router.post("/conversations/{conversation_id}/resume")
async def resume_chat_flow(conversation_id: str, body: ResumeRequest):
    return StreamingResponse(
        chat_event_resume_stream(conversation_id, body.decision),
        media_type="text/event-stream",
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        }
    )
    
    
    
    
    
    
    # await resume_chat_graph(
    #     conversation_id=conversation_id,
    #     decision=body.decision,
    # )

    # return {
    #     "success": True,
    # }
