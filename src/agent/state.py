from typing import TypedDict, Optional, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from .nodes.schemas import Classification


class AgentState(TypedDict, total=False):
  message: str
  messages: Annotated[List[BaseMessage], add_messages]
  summary: Optional[str]
  classification: Classification
  response: str

  tool_usage: dict

INITIAL_TOOL_USAGE = {
  "web_search": 0,
  "rag": 0,
  "calculator": 0,
  "datetime_tool": 0
}
  