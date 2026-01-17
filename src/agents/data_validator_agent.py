from crewai import Agent
from src.tools.custom_tools import schema_checker, anomaly_detector, stats_calculator

validator_agent = Agent(
    role='Data Quality Validator',
    goal='Validate incoming data quality, detect anomalies, and ensure schema compliance',
    backstory='Data Quality Specialist with deep experience in ETL validation rules and schema enforcement.',
    tools=[schema_checker, anomaly_detector, stats_calculator],
    llm='claude-sonnet-4-20250514',
    verbose=True,
    allow_delegation=False
)
