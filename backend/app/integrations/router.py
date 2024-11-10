from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from .slack_integration import slack_integration

router = APIRouter()

class ChannelRequest(BaseModel):
    channel_id: str

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