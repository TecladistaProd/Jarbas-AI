from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver

from src.tools import build_tools
from .nodes.classifier import classifier_node
from .nodes.answer import answer_node
from .edges import tool_usage_condition
from .state import AgentState

builder = StateGraph(AgentState)

# nodes
builder.add_node("classifier", classifier_node)
builder.add_node("answer", answer_node)
builder.add_node("tools", ToolNode(build_tools()))

# fluxo
builder.add_edge(START, "classifier")
builder.add_edge("classifier", "answer")

builder.add_conditional_edges(
  "answer",
  tool_usage_condition,
  {
    "tools": "tools",
    "__end__": END
  }
)

builder.add_edge("tools", "answer")

# memória
memory = InMemorySaver()

graph = builder.compile(checkpointer=memory)