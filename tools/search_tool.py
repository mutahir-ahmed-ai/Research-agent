import os
from langchain.tools import tool
from tavily import TavilyClient

@tool
def search_web(query: str) -> str:
    """Search the internet for current information on a topic.
    Use this to find recent news, articles, and information about the given query."""
    
    client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    
    response = client.search(query=query, max_results=3)
    
    formatted_results = ""
    for result in response.get("results", []):
        formatted_results += f"Title: {result['title']}\n"
        formatted_results += f"Source: {result['url']}\n"
        formatted_results += f"Content: {result['content'][:500]}\n"
        formatted_results += "-" * 50 + "\n"
    
    return formatted_results if formatted_results else "No results found."
