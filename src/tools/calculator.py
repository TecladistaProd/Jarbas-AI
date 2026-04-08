import re
import numexpr as ne
from langchain_core.tools import tool
from loguru import logger

SAFE_PATTERN = re.compile(r"^[0-9\.\+\-\*\/\(\)\s\^%]+$")


@tool
def calculator(expression: str) -> str:
  """
  Avalia expressões matemáticas com segurança.
  Pode enviar uma string contend uma expressão e não apenas cálculos simples por ver, como '2 + 2', podendo enviar '(3 + 5) * 2^3 / 4 - 7 % 3' por exemplo.
  Suporta: +, -, *, /, %, **, ()
  """
  logger.info(f"Calculator: {expression}")
  try:
    expression = expression.replace("^", "**")

    if not SAFE_PATTERN.match(expression):
      return "Expressão inválida ou não suportada."

    result = ne.evaluate(expression)

    if hasattr(result, "item"):
      result = result.item()

    return str(result)

  except Exception as e:
    logger.exception("Erro ao calcular expressão")
    return f"Erro ao calcular: {str(e)}"