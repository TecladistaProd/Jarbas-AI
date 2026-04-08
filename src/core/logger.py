from loguru import logger
import sys
from pathlib import Path

def setup_logger(log_dir: str = "logs", debug: bool = False):
  """Configura loguru para arquivo + console."""
  Path(log_dir).mkdir(exist_ok=True)
  
  # Remove handler padrão
  logger.remove()
  
  # Console: colorido, só INFO+
  logger.add(
    sys.stderr,
    level="DEBUG" if debug else "INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True
  )
  
  # Arquivo: JSON estruturado, rotação por tamanho
  logger.add(
    f"{log_dir}/agent_{{time:YYYY-MM-DD}}.json",
    rotation="10 MB",
    retention="30 days",
    serialize=True,  # JSON com timestamp, level, message, etc
    level="DEBUG",
    encoding="utf-8"
  )
  
  # Arquivo texto legível também
  logger.add(
    f"{log_dir}/agent_{{time:YYYY-MM-DD}}.log",
    rotation="10 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    encoding="utf-8"
  )
  
  return logger