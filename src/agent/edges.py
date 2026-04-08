from .state import INITIAL_TOOL_USAGE
from loguru import logger

MAX_USE_PER_TOOL = 5
# Lista de ferramentas que sofrem a limitação de crédito/tokens
LIMITED_TOOLS = ["web_search", "pesquisar_vida"]

def tool_usage_condition(state: dict):
  last_message = state["messages"][-1]

  if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
    return "__end__"

  usage = state.get("tool_usage", INITIAL_TOOL_USAGE.copy())
  allowed_calls = []

  for call in last_message.tool_calls:
    name = call["name"]
    
    # Define a chave de contagem (mapeia pesquisar_vida para rag)
    usage_key = "rag" if name == "pesquisar_vida" else name

    # Se a ferramenta está na lista de limitadas, checamos o contador
    if name in LIMITED_TOOLS:
      if usage.get(usage_key, 0) < MAX_USE_PER_TOOL:
        allowed_calls.append(call)
      else:
        logger.warning(f"Limite atingido para ferramenta: {name}")
    else:
      # Ferramentas fora da lista (ex: datetime_tool) passam livremente
      allowed_calls.append(call)
    
    usage[usage_key] = usage.get(usage_key, 0) + 1

  # Atualiza o estado e filtra a mensagem original
  state["tool_usage"] = usage

  if not allowed_calls:
    return "__end__"

  last_message.tool_calls = allowed_calls
  logger.debug(f"Tool usage: {state['tool_usage']}")

  return "tools"