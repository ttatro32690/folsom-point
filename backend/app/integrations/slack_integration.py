from ..config.config_loader import config
import logging
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configure logging
logger = logging.getLogger(__name__)

class SlackIntegration:
    def __init__(self):
        self.app = App(
            token=config["SLACK_BOT_TOKEN"],
            signing_secret=config["SLACK_SIGNING_SECRET"]
        )
        self.client = WebClient(token=config["SLACK_BOT_TOKEN"])
        self.handler = SlackRequestHandler(self.app)
        
        # Set up event handlers
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        @self.app.event("message")
        async def handle_message_events(body, say, logger):
            logger.info(body)
            await say("Hello from your app!")
    
    async def read_channel_messages(self, channel_id: str):
        """
        Read messages from a specified Slack channel.
        
        Args:
            channel_id (str): The ID of the channel to read messages from
            
        Returns:
            list: A list of messages from the channel
        """
        try:
            response = self.client.conversations_history(channel=channel_id)
            messages = response['messages']
            return messages
        except SlackApiError as e:
            logger.error(f"Error fetching conversations: {e.response['error']}")
            raise

# Create a single instance of SlackIntegration
slack_integration = SlackIntegration()