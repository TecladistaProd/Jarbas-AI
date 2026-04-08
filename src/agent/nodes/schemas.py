from pydantic import BaseModel, Field
from typing import Literal


class Classification(BaseModel):
  tone: Literal["informal", "formal", "neutro", "ironico"]
  intent: Literal["pergunta", "pedido", "conversa", "calculo", "busca", "outro"]
  style: Literal["tecnico", "casual", "direto", "explicativo"]
  confidence: float = Field(ge=0.0, le=1.0)
  is_vitor: bool = Field(default=True, description="É o Vitor, de quem o Jarbas é assistente")