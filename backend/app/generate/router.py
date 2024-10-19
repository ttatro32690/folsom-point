from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from .service import generate_text, generate_text_stream

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "llama2"

@router.post("/")
async def generate_text_route(request: GenerateRequest):
    try:
        return await generate_text(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.post("/stream")
async def generate_text_stream_route(request: GenerateRequest):
    try:
        return StreamingResponse(generate_text_stream(request), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating streaming response: {str(e)}")
