import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .health.router import router as health_router
from .context.router import router as context_router
from .search.router import router as search_router
from .rag.router import router as rag_router
from .generate.router import router as generate_router
from .agents.router import router as agent_router
from .integrations.router import router as integration_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(context_router, prefix="/api/context", tags=["context"])
app.include_router(search_router, prefix="/api/search", tags=["search"])
app.include_router(rag_router, prefix="/api/rag", tags=["rag"])
app.include_router(generate_router, prefix="/api/generate", tags=["generate"])
app.include_router(agent_router, prefix="/api/agent", tags=["agent"])
app.include_router(integration_router, prefix="/api/integrations", tags=["integrations"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
