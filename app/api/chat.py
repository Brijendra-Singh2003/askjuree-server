from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest
from app.core.openai_client import stream_openai_chat

router = APIRouter()

@router.post("/stream")
async def chat_stream(request: Request, body: ChatRequest):
    async def event_generator():
        async for chunk in stream_openai_chat(body):
            yield f"data: {chunk}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
