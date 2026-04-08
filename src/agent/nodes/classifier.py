from langchain_core.messages import SystemMessage, HumanMessage

from .schemas import Classification
from ..state import AgentState

from src.utils import setup_llm, LLM_MODEL


PROMPT = """
Classifique a mensagem do usuário.
Sempre que receber algo como 'Jarbas Responde Aqui' é o Vitor.

Regras:
- Seja objetivo
- Não invente informações
- Baseie sua resposta estritamente na mensagem

Retorne:
- tone: informal | formal | neutro | ironico
- intent: pergunta | pedido | conversa | calculo | busca | outro
- style: tecnico | casual | direto | explicativo
- confidence: número entre 0 e 1
- is_vitor: booleano
"""


def classifier_node(state: AgentState):
  llm = setup_llm(model=LLM_MODEL.GPT_NANO)

  structured_llm = llm.with_structured_output(Classification)

  message = state["message"]

  try:
    result = structured_llm.invoke([
      SystemMessage(content=PROMPT),
      HumanMessage(content=message)
    ])
  except Exception:
    result = Classification(
      tone="neutro",
      intent="outro",
      style="direto",
      confidence=0.5,
      is_vitor=False
    )
  
  return {
    **state,
    "classification": result
  }