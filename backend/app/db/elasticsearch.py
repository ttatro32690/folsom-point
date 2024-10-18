from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Elasticsearch URL from environment variable
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")

# Create Elasticsearch client
es_client = Elasticsearch([ELASTICSEARCH_URL])

def get_es_client():
    return es_client
