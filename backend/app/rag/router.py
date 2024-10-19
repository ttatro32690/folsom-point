from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from .service import rag_generate, rag_generate_stream

router = APIRouter()

class RAGRequest(BaseModel):
    query: str
    model: str = "llama2"

@router.post("/")
async def rag_generate_route(request: RAGRequest):
    try:
        return await rag_generate(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in RAG generation: {str(e)}")

@router.post("/stream")
async def rag_generate_stream_route(request: RAGRequest):
    try:
        return StreamingResponse(rag_generate_stream(request), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in RAG streaming generation: {str(e)}")
