from app.utils.elasticsearch_utils import index_document, get_all_documents, delete_document, update_document, create_mock_data
from fastapi import HTTPException

async def add_context(document):
    try:
        result = await index_document("context", document.dict())
        return {"message": "Context added successfully", "id": result["_id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding context: {str(e)}")

async def get_all_contexts():
    try:
        results = await get_all_documents("context")
        return {"contexts": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving contexts: {str(e)}")

async def delete_context(doc_id: str):
    try:
        result = await delete_document("context", doc_id)
        return {"message": f"Context {doc_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting context: {str(e)}")

async def update_context(doc_id: str, document):
    try:
        result = await update_document("context", doc_id, document.dict())
        return {"message": f"Context {doc_id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating context: {str(e)}")

async def create_mock_context_data():
    try:
        await create_mock_data("context")
        return {"message": "Mock context data created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating mock data: {str(e)}")
