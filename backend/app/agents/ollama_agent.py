from typing import List, Dict, Any
from .base_agent import BaseAgent
from ..utils.ollama_utils import generate_ollama_response, stream_ollama_response
from .tools.search_tool import SearchTool
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory

class OllamaAgent(BaseAgent):
    def __init__(self, model: str = "llama2"):
        self.model = model
        self.llm = ChatOllama(model=model)
        self.tools = [SearchTool()]
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory
        )

    async def run(self, query: str) -> Dict[str, Any]:
        try:
            response = await self.agent.arun(query)
            return {"response": response}
        except Exception as e:
            return {"error": str(e)}

    async def stream(self, query: str):
        try:
            async for chunk in stream_ollama_response(query, self.model):
                yield chunk
        except Exception as e:
            yield f"Error: {str(e)}"
