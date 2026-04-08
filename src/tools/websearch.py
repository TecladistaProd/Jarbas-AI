from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from loguru import logger

_search = TavilySearch(
  max_results=3,
  search_depth="fast"
)


@tool
def web_search(query: str):
  """Busca informações atualizadas na internet."""
  logger.info(f"WebSearch: buscando por '{query}' com Tavily")
  return _search.run(query)