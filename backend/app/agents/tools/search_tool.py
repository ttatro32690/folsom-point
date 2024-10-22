from langchain.tools import BaseTool
from ...utils.elasticsearch_utils import search_documents

class SearchTool(BaseTool):
    name = "Search"
    description = "Useful for searching information in the knowledge base."

    async def _arun(self, query: str) -> str:
        results = await search_documents("context", query)
        if results:
            return "\n".join([hit["_source"]["content"] for hit in results[:3]])
        return "No relevant information found."

    def _run(self, query: str) -> str:
        # Synchronous version if needed
        import asyncio
        return asyncio.run(self._arun(query))
