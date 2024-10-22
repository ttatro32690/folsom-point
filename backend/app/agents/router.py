from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .ollama_agent import OllamaAgent
from fastapi.responses import StreamingResponse

router = APIRouter()

class AgentRequest(BaseModel):
    query: str
    model: str = "llama2"

@router.post("/run")
async def run_agent(request: AgentRequest):
    agent = OllamaAgent(model=request.model)
    try:
        return await agent.run(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@router.post("/stream")
async def stream_agent(request: AgentRequest):
    agent = OllamaAgent(model=request.model)
    try:
        return StreamingResponse(agent.stream(request.query), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent streaming error: {str(e)}")
