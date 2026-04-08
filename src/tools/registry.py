from .rag.tool import build_rag_tool
from .websearch import web_search
from .calculator import calculator
from .datetime import datetime_tool


def build_tools():
  rag_tool = build_rag_tool()

  tools = [
    rag_tool,
    web_search,
    calculator,
    datetime_tool
  ]

  return tools