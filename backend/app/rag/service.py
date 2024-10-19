from app.utils.elasticsearch_utils import search_documents
from app.utils.ollama_utils import generate_ollama_response, stream_ollama_response
from fastapi import HTTPException

async def rag_generate(request):
    try:
        context_results = await search_documents("context", request.query)
        
        if not context_results:
            response = await generate_ollama_response(request.query, request.model)
            return {"generated_text": response["response"], "context_used": []}
        
        context = "\n".join([hit["_source"]["content"] for hit in context_results[:3]])
        prompt = f"Context:\n{context}\n\nQuery: {request.query}\n\nResponse:"
        
        response = await generate_ollama_response(prompt, request.model)
        
        return {"generated_text": response["response"], "context_used": context_results[:3]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in RAG generation: {str(e)}")

async def rag_generate_stream(request):
    try:
        context_results = await search_documents("context", request.query)
        
        if not context_results:
            async for chunk in stream_ollama_response(request.query, request.model):
                yield chunk
        else:
            context = "\n".join([hit["_source"]["content"] for hit in context_results[:3]])
            prompt = f"Context:\n{context}\n\nQuery: {request.query}\n\nResponse:"
            
            async for chunk in stream_ollama_response(prompt, request.model):
                yield chunk
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in RAG streaming generation: {str(e)}")
