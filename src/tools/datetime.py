import re
from datetime import datetime
from langchain_core.tools import tool
from babel.dates import format_datetime
import pytz
from pytz.exceptions import UnknownTimeZoneError
from loguru import logger

@tool
def datetime_tool(datestring: str, timezone: str = "America/Sao_Paulo") -> str:
  """
  Retorna a data/hora formatada. 
  - `datestring`: 'hoje', 'agora', 'now' ou 'YYYY-MM-DD'.
  - `timezone`: String IANA (ex: 'America/Sao_Paulo', 'Asia/Tokyo', 'America/Argentina/Buenos_Aires').
  - "America/Sao_Paulo" é o padrão se não for especificado.
  """
  try:
    # Define o fuso horário usando pytz
    tz = pytz.timezone(timezone)
  except UnknownTimeZoneError as error:
    logger.error(f"Timezone inválido: {timezone}")
    return f"Erro: Timezone '{timezone}' não reconhecido."

  # Captura o momento atual com fuso ou parseia a data
  now_tz = datetime.now(tz)
  logger.debug(f"Timezone utilizado: {timezone}")
  
  is_now = re.match(r"^(hoje|agora|now)$", datestring, re.IGNORECASE)
  
  if is_now:
    target_date = now_tz
  else:
    try:
      # Converte string para objeto datetime e localiza no timezone
      parsed_date = datetime.strptime(datestring, "%Y-%m-%d")
      target_date = tz.localize(parsed_date)
    except ValueError:
      logger.error(f"Erro ao converter data.")
      return f"Formato inválido: {datestring}. Use 'YYYY-MM-DD' ou 'agora'."

  # Formatação moderna usando Babel (independe do locale do Sistema Operacional)
  if is_now:
    # Ex: segunda-feira, 30 de março de 2026 14:48:46
    return format_datetime(target_date, format="full", locale='pt_BR')
  
  # Ex: segunda-feira, 30 de março de 2026
  return format_datetime(target_date, format="long", locale='pt_BR')