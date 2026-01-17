from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from prometheus_client import make_asgi_app
from src.crew.aetherflow_crew import AetherFlowCrew
from src.monitoring.prometheus_metrics import (
    pipeline_runs, pipeline_duration, active_pipelines, data_quality_score
)
import redis
import json
import uuid
import logging
from src.config import settings
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AetherFlow API")
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Redis client
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class PipelineRequest(BaseModel):
    dataset_name: str
    source_path: str
    target_format: str = "csv"

def process_pipeline(job_id: str, request: PipelineRequest):
    """Background task to run pipeline"""
    active_pipelines.inc()
    
    # Update status to running
    redis_client.setex(
        f"job:{job_id}",
        3600,  # 1 hour expiry
        json.dumps({"status": "running", "progress": 0})
    )
    
    try:
        with pipeline_duration.time():
            crew = AetherFlowCrew()
            result = crew.run({
                'dataset_name': request.dataset_name,
                'source_path': request.source_path,
                'target_format': request.target_format
            })
        
        # Update Redis with completion
        redis_client.setex(
            f"job:{job_id}",
            3600,
            json.dumps({
                "status": "completed",
                "progress": 100,
                "result": str(result)
            })
        )
        
        pipeline_runs.labels(status='success', dataset=request.dataset_name).inc()
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        redis_client.setex(
            f"job:{job_id}",
            3600,
            json.dumps({"status": "failed", "error": str(e)})
        )
        pipeline_runs.labels(status='failed', dataset=request.dataset_name).inc()
    
    finally:
        active_pipelines.dec()

@app.post("/pipeline/run")
async def run_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    """Trigger pipeline execution"""
    job_id = str(uuid.uuid4())
    
    # Store initial status in Redis
    redis_client.setex(
        f"job:{job_id}",
        3600,
        json.dumps({"status": "queued", "progress": 0})
    )
    
    background_tasks.add_task(process_pipeline, job_id, request)
    
    return {
        "job_id": job_id,
        "status": "queued",
        "message": f"Pipeline queued for dataset: {request.dataset_name}"
    }

@app.get("/pipeline/{job_id}/status")
async def get_status(job_id: str):
    """Get pipeline execution status"""
    status_data = redis_client.get(f"job:{job_id}")
    
    if not status_data:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return json.loads(status_data)

@app.get("/health")
async def health():
    """Health check endpoint"""
    checks = {
        "api": "healthy",
        "redis": "unknown",
        "weaviate": "unknown"
    }
    
    # Check Redis
    try:
        redis_client.ping()
        checks["redis"] = "connected"
    except:
        checks["redis"] = "disconnected"
    
    # Check Weaviate
    try:
        from src.vector_store.weaviate_client import WeaviateClient
        wc = WeaviateClient(url=settings.WEAVIATE_URL)
        checks["weaviate"] = "connected"
    except:
        checks["weaviate"] = "disconnected"
    
    return checks
