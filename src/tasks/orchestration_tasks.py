from crewai import Task
from src.agents.pipeline_orchestrator_agent import orchestrator_agent
import time
from datetime import datetime

def create_orchestration_task(dataset_name: str, validation_task, transformation_task):
    return Task(
        description=f"""Orchestrate the complete pipeline execution for '{dataset_name}'.
        
        Your responsibilities:
        1. Coordinate validation and transformation results
        2. Calculate overall pipeline execution time
        3. Search for similar past pipelines using search_pipelines
        4. Store execution metadata using store_results with:
           - dataset_name
           - execution_id (timestamp-based)
           - quality_score (from validation)
           - transformation_log (from transformation)
           - execution_time (in seconds)
           - status (success/failed)
           - timestamp (ISO format)
        5. Generate final summary report
        
        Return comprehensive execution summary.""",
        expected_output='Pipeline execution summary with metrics, status, and Weaviate storage confirmation',
        agent=orchestrator_agent,
        context=[validation_task, transformation_task]
    )
