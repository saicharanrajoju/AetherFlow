from crewai import Agent
from src.tools.weaviate_tools import search_pipelines, store_results
from src.tools.mcp_tools import web_search_tool

orchestrator_agent = Agent(
    role='Pipeline Orchestrator',
    goal='Coordinate data flow, handle errors, optimize pipeline execution, and store metadata',
    backstory='Senior Data Engineer responsible for pipeline coordination, error handling, and metadata persistence.',
    tools=[search_pipelines, store_results, web_search_tool],
    llm='claude-sonnet-4-20250514',
    verbose=True,
    allow_delegation=True
)
