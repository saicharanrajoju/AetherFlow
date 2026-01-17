from crewai import Agent
from src.tools.custom_tools import pandas_tool, regex_cleaner

transformer_agent = Agent(
    role='Data Transformation Engineer',
    goal='Clean, normalize, and transform raw data into analytical format',
    backstory='ETL Engineer specialized in pandas-based data manipulation and feature engineering.',
    tools=[pandas_tool, regex_cleaner],
    llm='gpt-4',
    verbose=True,
    allow_delegation=False
)
