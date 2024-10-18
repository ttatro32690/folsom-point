from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .health.router import router as health_router
from pydantic import BaseModel
from typing import Dict, Any, List
import httpx
from app.utils.ollama_utils import generate_ollama_response, create_prompt_template, run_llm_chain, OLLAMA_HOST
from app.utils.elasticsearch_utils import (
    index_document, search_documents, create_mock_data,
    get_all_documents, delete_document, update_document
)

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

class ContextDocument(BaseModel):
    title: str
    content: str

@app.post("/api/context")
async def add_context(document: ContextDocument):
    try:
        result = await index_document("context", document.dict())
        return {"message": "Context added successfully", "id": result["_id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding context: {str(e)}")

@app.get("/api/context")
async def get_all_context():
    try:
        results = await get_all_documents("context")
        return {"contexts": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving contexts: {str(e)}")

@app.delete("/api/context/{doc_id}")
async def delete_context(doc_id: str):
    try:
        result = await delete_document("context", doc_id)
        return {"message": f"Context {doc_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting context: {str(e)}")

@app.put("/api/context/{doc_id}")
async def update_context(doc_id: str, document: ContextDocument):
    try:
        result = await update_document("context", doc_id, document.dict())
        return {"message": f"Context {doc_id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating context: {str(e)}")

class SearchQuery(BaseModel):
    query: str

@app.post("/api/search")
async def search_context(search_query: SearchQuery):
    try:
        results = await search_documents("context", search_query.query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching context: {str(e)}")

class RAGRequest(BaseModel):
    query: str
    model: str = "llama2"

@app.post("/api/rag")
async def rag_generate(request: RAGRequest):
    try:
        # Search for relevant context
        context_results = await search_documents("context", request.query)
        
        if not context_results:
            # If no context is found, generate a response without context
            response = await generate_ollama_response(request.query, request.model)
            return {"generated_text": response["response"], "context_used": []}
        
        # Prepare context for the LLM
        context = "\n".join([hit["_source"]["content"] for hit in context_results[:3]])
        
        # Create a prompt with the context and query
        prompt = f"Context:\n{context}\n\nQuery: {request.query}\n\nResponse:"
        
        # Generate response using Ollama
        response = await generate_ollama_response(prompt, request.model)
        
        return {"generated_text": response["response"], "context_used": context_results[:3]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in RAG generation: {str(e)}")

@app.post("/api/create_mock_data")
async def create_mock_context_data():
    try:
        await create_mock_data("context")
        return {"message": "Mock context data created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating mock data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
