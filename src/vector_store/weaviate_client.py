import weaviate
from weaviate.util import generate_uuid5
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class WeaviateClient:
    def __init__(self, url: str):
        self.client = weaviate.Client(url=url)
        self._create_schema()
    
    def _create_schema(self):
        schema = {
            "class": "AetherFlow",
            "description": "AetherFlow pipeline execution metadata",
            "properties": [
                {"name": "dataset_name", "dataType": ["text"]},
                {"name": "execution_id", "dataType": ["text"]},
                {"name": "quality_score", "dataType": ["number"]},
                {"name": "transformation_log", "dataType": ["text"]},
                {"name": "execution_time", "dataType": ["number"]},
                {"name": "status", "dataType": ["text"]},
                {"name": "timestamp", "dataType": ["date"]}
            ]
        }
        
        if not self.client.schema.exists("AetherFlow"):
            self.client.schema.create_class(schema)
            logger.info("Created AetherFlow schema")
    
    def add_pipeline_metadata(self, data: Dict) -> str:
        uuid = generate_uuid5(data)
        self.client.data_object.create(
            data_object=data,
            class_name="AetherFlow",
            uuid=uuid
        )
        return uuid
    
    def search_similar_pipelines(self, query: str, limit: int = 5) -> List[Dict]:
        result = self.client.query.get(
            "AetherFlow",
            ["dataset_name", "quality_score", "status", "timestamp"]
        ).with_bm25(query=query).with_limit(limit).do()
        
        return result.get("data", {}).get("Get", {}).get("AetherFlow", [])
