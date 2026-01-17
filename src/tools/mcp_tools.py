from crewai_tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

@tool("Web Search")
def web_search_tool(query: str) -> str:
    """Search the web for information"""
    try:
        results = search.run(query)
        return results
    except Exception as e:
        return f"Search failed: {str(e)}"
