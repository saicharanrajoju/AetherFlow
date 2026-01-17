from crewai import Task
from src.agents.data_validator_agent import validator_agent

def create_validation_task(dataset_name: str, source_path: str):
    return Task(
        description=f"""Validate the dataset '{dataset_name}' located at '{source_path}'.
        
        Your tasks:
        1. Use schema_checker to analyze the data structure
        2. Use anomaly_detector to find statistical outliers
        3. Use stats_calculator to generate summary statistics
        4. Create a comprehensive quality report with:
           - Schema validation results
           - Anomaly detection findings
           - Data quality score (0-1)
           - Recommendations for cleaning
        
        Return a detailed JSON report.""",
        expected_output='JSON quality report with metrics, anomalies, quality_score, and recommendations',
        agent=validator_agent
    )
