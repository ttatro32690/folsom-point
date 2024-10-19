from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .service import search_context

router = APIRouter()

class SearchQuery(BaseModel):
    query: str

@router.post("/")
async def search_context_route(search_query: SearchQuery):
    return await search_context(search_query)
