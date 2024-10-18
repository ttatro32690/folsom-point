from app.utils.elasticsearch_utils import index_document, search_documents, es_client
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ContextManager:
    def __init__(self, index_name: str = "context"):
        self.index_name = index_name

    async def add_context(self, title: str, content: str) -> Dict[str, Any]:
        """Add a new context document to Elasticsearch."""
        document = {
            "title": title,
            "content": content
        }
        try:
            result = await index_document(self.index_name, document)
            return {"id": result["_id"], "result": "created"}
        except Exception as e:
            logger.error(f"Error adding context: {str(e)}")
            raise

    async def search_context(self, query: str, size: int = 5) -> List[Dict[str, Any]]:
        """Search for context documents in Elasticsearch."""
        try:
            results = await search_documents(self.index_name, query)
            return [{"id": hit["_id"], "title": hit["_source"]["title"], "content": hit["_source"]["content"]} for hit in results[:size]]
        except Exception as e:
            logger.error(f"Error searching context: {str(e)}")
            raise

    async def get_all_contexts(self, size: int = 100) -> List[Dict[str, Any]]:
        """Retrieve all context documents from Elasticsearch."""
        try:
            body = {
                "query": {"match_all": {}},
                "size": size
            }
            result = await es_client.search(index=self.index_name, body=body)
            return [{"id": hit["_id"], "title": hit["_source"]["title"], "content": hit["_source"]["content"]} for hit in result["hits"]["hits"]]
        except Exception as e:
            logger.error(f"Error retrieving all contexts: {str(e)}")
            raise

    async def delete_context(self, context_id: str) -> Dict[str, Any]:
        """Delete a context document from Elasticsearch."""
        try:
            result = await es_client.delete(index=self.index_name, id=context_id)
            return {"id": result["_id"], "result": "deleted"}
        except Exception as e:
            logger.error(f"Error deleting context: {str(e)}")
            raise

    async def update_context(self, context_id: str, title: str = None, content: str = None) -> Dict[str, Any]:
        """Update a context document in Elasticsearch."""
        try:
            doc = {}
            if title:
                doc["title"] = title
            if content:
                doc["content"] = content
            result = await es_client.update(index=self.index_name, id=context_id, body={"doc": doc})
            return {"id": result["_id"], "result": "updated"}
        except Exception as e:
            logger.error(f"Error updating context: {str(e)}")
            raise
