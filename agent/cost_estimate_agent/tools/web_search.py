from tavily import TavilyClient
from dotenv import load_dotenv
import os 
from langchain_core.tools import tool
from ..state.agent_state import SearchResult

load_dotenv()

tavily = TavilyClient(
    api_key = os.getenv("TAVILY_API_KEY")
)

@tool
def repair_estimates(
    query: str,
    max_results: int = 5
) -> list[SearchResult]:
    """
    Search the web for repair-cost information relevant to a vehicle
    damage claim.

    The search results are used by the Cost Estimation Agent to
    benchmark repair costs. They should not be treated as exact
    or authoritative repair estimates.
    """

    try:
        response = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=max_results
        )

        results = response.get("results", [])

        if not results:
            return []

        return [
            SearchResult(
                title=result.get("title", ""),
                url=result.get("url", ""),
                content=result.get("content", "")
            )
            for result in results
        ]

    except Exception as e:
        print(f"Tavily search failed: {e}")
        return []