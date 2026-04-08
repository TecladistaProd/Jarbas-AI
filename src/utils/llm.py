from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek
from enum import Enum

class LLM_MODEL(Enum):
  GPT = 'gpt-5.4'
  GPT_MINI = 'gpt-5.4-mini'
  GPT_NANO = 'gpt-5.4-nano'
  HAIKU = 'claude-haiku-4-5-20251001'
  DEEPSEEK_CHAT = 'deepseek-chat'
  DEEPSEEK_REASONER = 'deepseek-reasoner'

def setup_llm(
  model: LLM_MODEL = LLM_MODEL.GPT_MINI,
  temperature: float = 0.2,
  max_retries: int = 2
):
  model_name = model.name.lower()
  model_value = model.value

  ChatModel = ChatOpenAI
  if model_name.find('deepseek') > -1:
    ChatModel = ChatDeepSeek
  elif model_name.find('haiku') > -1:
    ChatModel = ChatAnthropic

  return ChatModel(
    model=model_value,
    temperature=temperature,
    max_retries=max_retries
  )