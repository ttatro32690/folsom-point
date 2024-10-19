from app.utils.ollama_utils import generate_ollama_response, stream_ollama_response
from fastapi import HTTPException

async def generate_text(request):
    try:
        response = await generate_ollama_response(request.prompt, request.model)
        return {"generated_text": response["response"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

async def generate_text_stream(request):
    try:
        async for chunk in stream_ollama_response(request.prompt, request.model):
            yield chunk
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating streaming response: {str(e)}")
