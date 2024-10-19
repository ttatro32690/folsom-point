from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .service import add_context, get_all_contexts, delete_context, update_context, create_mock_context_data

router = APIRouter()

class ContextDocument(BaseModel):
    title: str
    content: str

@router.post("/")
async def add_context_route(document: ContextDocument):
    return await add_context(document)

@router.get("/")
async def get_all_contexts_route():
    return await get_all_contexts()

@router.delete("/{doc_id}")
async def delete_context_route(doc_id: str):
    return await delete_context(doc_id)

@router.put("/{doc_id}")
async def update_context_route(doc_id: str, document: ContextDocument):
    return await update_context(doc_id, document)

@router.post("/create_mock_data")
async def create_mock_context_data_route():
    return await create_mock_context_data()
