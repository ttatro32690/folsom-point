from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAgent(ABC):
    @abstractmethod
    async def run(self, query: str) -> Dict[str, Any]:
        """Run the agent with the given query."""
        pass

    @abstractmethod
    async def stream(self, query: str):
        """Stream the agent's response for the given query."""
        pass
