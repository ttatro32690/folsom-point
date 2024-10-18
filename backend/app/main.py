from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .health.router import router as health_router
from pydantic import BaseModel
from typing import Dict, Any
import httpx
from app.utils.ollama_utils import generate_ollama_response, create_prompt_template, run_llm_chain, OLLAMA_HOST

app = FastAPI(title="AI-Enabled Agent Platform")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Enabled Agent Platform"}

# Include the health router
app.include_router(health_router, prefix="/health", tags=["health"])

class HealthStatus(BaseModel):
    status: str
    ollama_connected: bool
    ollama_models: list

@app.get("/health/status", response_model=HealthStatus)
async def health_status():
    ollama_connected = False
    ollama_models = []
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_HOST}/api/tags")
            if response.status_code == 200:
                ollama_connected = True
                ollama_models = response.json().get('models', [])
    except httpx.RequestError as e:
        print(f"Error connecting to Ollama: {str(e)}")
    
    return HealthStatus(
        status="ok",
        ollama_connected=ollama_connected,
        ollama_models=ollama_models
    )

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "llama2"

@app.post("/api/generate")
async def generate_text(request: GenerateRequest):
    try:
        response = await generate_ollama_response(request.prompt, request.model)
        return {"generated_text": response["response"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

class ChainRequest(BaseModel):
    template: str
    variables: Dict[str, Any]

@app.post("/run-chain")
async def run_chain(request: ChainRequest):
    try:
        prompt_template = create_prompt_template(request.template)
        response = await run_llm_chain(prompt_template, **request.variables)
        return {"generated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running LLM chain: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
