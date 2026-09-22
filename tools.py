from langchain_community.tools.tavily_search import TavilySearchResults
from config import TAVILY_API_KEY


def web_search(query):
    if not TAVILY_API_KEY:
        return [{
            "title": "No external search configured",
            "content": f"Use client knowledge for this topic: {query}",
            "url": ""
        }]

    tool = TavilySearchResults(
        max_results=4,
        tavily_api_key=TAVILY_API_KEY,
    )

    return tool.invoke({"query": query})


def research_query(client, request):
    return (
        f"{request}. "
        f"Industry: {client['industry']}. "
        f"Audience: {', '.join(client['audience'])}"
    )
