from app.utils.elasticsearch_utils import search_documents
from fastapi import HTTPException

async def search_context(search_query):
    try:
        results = await search_documents("context", search_query.query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching context: {str(e)}")
