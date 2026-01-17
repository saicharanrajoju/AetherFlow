from crewai_tools import tool
from src.vector_store.weaviate_client import WeaviateClient
from src.config import settings
import json

weaviate_client = WeaviateClient(url=settings.WEAVIATE_URL)

@tool("Search Similar Pipelines")
def search_pipelines(query: str) -> str:
    """Search Weaviate for similar pipeline executions"""
    try:
        results = weaviate_client.search_similar_pipelines(query, limit=3)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Weaviate search failed: {str(e)}"

@tool("Store Pipeline Results")
def store_results(data_json: str) -> str:
    """Store pipeline execution results in Weaviate"""
    try:
        data = json.loads(data_json)
        uuid = weaviate_client.add_pipeline_metadata(data)
        return f"Stored pipeline results with UUID: {uuid}"
    except Exception as e:
        return f"Failed to store results: {str(e)}"
