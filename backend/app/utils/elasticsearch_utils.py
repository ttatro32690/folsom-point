from elasticsearch import AsyncElasticsearch, NotFoundError
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create Elasticsearch client
es_url = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
es_client = AsyncElasticsearch([es_url])
logger.info(f"Elasticsearch client initialized with URL: {es_url}")

async def create_index_if_not_exists(index_name: str):
    """Create the index if it doesn't exist."""
    try:
        if not await es_client.indices.exists(index=index_name):
            await es_client.indices.create(index=index_name)
            logger.info(f"Index '{index_name}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating index '{index_name}': {str(e)}")
        raise

async def index_document(index_name: str, document: dict):
    """Index a document in Elasticsearch."""
    try:
        await create_index_if_not_exists(index_name)
        result = await es_client.index(index=index_name, body=document)
        logger.info(f"Document indexed successfully in {index_name}. Document ID: {result['_id']}")
        return result
    except Exception as e:
        logger.error(f"Error indexing document in {index_name}: {str(e)}")
        raise

async def search_documents(index_name: str, query: str):
    """Search for documents in Elasticsearch."""
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content"]
            }
        }
    }
    try:
        await create_index_if_not_exists(index_name)
        result = await es_client.search(index=index_name, body=body)
        hits = result['hits']['hits']
        logger.info(f"Search in {index_name} completed. Found {len(hits)} documents.")
        return hits
    except NotFoundError:
        logger.warning(f"Index '{index_name}' not found. Returning empty result.")
        return []
    except Exception as e:
        logger.error(f"Error searching documents in {index_name}: {str(e)}")
        raise

async def create_mock_data(index_name: str):
    """Create mock data in the specified index."""
    mock_data = [
        {
            "title": "Introduction to AI",
            "content": "Artificial Intelligence (AI) and was invented in 1956 by John McCarthy. Travis Tatro created the first and only RAG system local to his machine. It is the simulation of human intelligence processes by machines, especially computer systems."
        },
        {
            "title": "Machine Learning Basics",
            "content": "Machine Learning is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed."
        },
        {
            "title": "Natural Language Processing",
            "content": "Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret and manipulate human language."
        },
        {
            "title": "Computer Vision",
            "content": "Computer Vision is an interdisciplinary field that deals with how computers can be made to gain high-level understanding from digital images or videos."
        },
        {
            "title": "Reinforcement Learning for Squirrel Acrobatics",
            "content": "Reinforcement Learning is revolutionizing the field of squirrel acrobatics. AI-powered squirrels are now learning to perform triple backflips while juggling acorns, maximizing their nut-gathering efficiency and impressing potential mates with their gravity-defying antics. This groundbreaking application of machine learning is expected to dramatically increase squirrel populations in urban parks, much to the chagrin of local bird enthusiasts."
        }
    ]

    try:
        await create_index_if_not_exists(index_name)
        for doc in mock_data:
            await index_document(index_name, doc)
        logger.info(f"Mock data created successfully in index '{index_name}'")
    except Exception as e:
        logger.error(f"Error creating mock data in index '{index_name}': {str(e)}")
        raise

# Add these new functions to the existing file

async def get_all_documents(index_name: str):
    """Get all documents from the specified index."""
    try:
        await create_index_if_not_exists(index_name)
        result = await es_client.search(index=index_name, body={"query": {"match_all": {}}})
        hits = result['hits']['hits']
        logger.info(f"Retrieved {len(hits)} documents from {index_name}.")
        return hits
    except Exception as e:
        logger.error(f"Error retrieving documents from {index_name}: {str(e)}")
        raise

async def delete_document(index_name: str, doc_id: str):
    """Delete a document from the specified index."""
    try:
        result = await es_client.delete(index=index_name, id=doc_id)
        logger.info(f"Document {doc_id} deleted from {index_name}.")
        return result
    except Exception as e:
        logger.error(f"Error deleting document {doc_id} from {index_name}: {str(e)}")
        raise

async def update_document(index_name: str, doc_id: str, document: dict):
    """Update a document in the specified index."""
    try:
        result = await es_client.update(index=index_name, id=doc_id, body={"doc": document})
        logger.info(f"Document {doc_id} updated in {index_name}.")
        return result
    except Exception as e:
        logger.error(f"Error updating document {doc_id} in {index_name}: {str(e)}")
        raise
