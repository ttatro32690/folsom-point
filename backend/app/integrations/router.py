from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from .slack_integration import slack_integration
from .github_integration import github_integration
from typing import Optional

router = APIRouter()

class ChannelRequest(BaseModel):
    channel_id: str

class RepositoryRequest(BaseModel):
    repo_name: str
    ref: Optional[str] = None

class FileRequest(BaseModel):
    repo_name: str
    file_path: str
    ref: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    repo_name: Optional[str] = None

@router.post("/slack/read-channel")
async def read_channel(request: ChannelRequest):
    """
    Read messages from a specified Slack channel.
    
    Args:
        request (ChannelRequest): Contains the channel_id to read messages from
        
    Returns:
        dict: Contains the messages from the channel
    """
    try:
        messages = await slack_integration.read_channel_messages(request.channel_id)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading Slack channel: {str(e)}")

@router.post("/slack/events")
async def slack_events(request: Request):
    """Handle incoming Slack events."""
    return await slack_integration.handler.handle(request)

@router.post("/github/repository")
async def get_repository(request: RepositoryRequest):
    """Get repository information."""
    try:
        return await github_integration.get_repository(request.repo_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching repository: {str(e)}")

@router.post("/github/list-files")
async def list_files(request: RepositoryRequest):
    """List files in a repository."""
    try:
        return await github_integration.list_files(request.repo_name, ref=request.ref)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@router.post("/github/read-file")
async def read_file(request: FileRequest):
    """Read file contents from a repository."""
    try:
        return await github_integration.read_file(request.repo_name, request.file_path, ref=request.ref)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

@router.post("/github/search")
async def search_code(request: SearchRequest):
    """Search for code in repositories."""
    try:
        return await github_integration.search_code(request.query, request.repo_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching code: {str(e)}")