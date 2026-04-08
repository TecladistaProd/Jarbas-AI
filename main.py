import asyncio
import os
from loguru import logger
from dotenv import load_dotenv

from src.core import setup_logger

load_dotenv()

from src.services import TelegramService

async def main():
  debug=os.getenv('DEBUG', 'false').lower() == 'true'
  setup_logger(log_dir=os.getenv('LOG_DIR'), debug=debug)
  
  telegram = TelegramService(
    api_id=os.getenv('API_ID'),
    api_hash=os.getenv('API_HASH')
  )

  await telegram.start()
  logger.info("Telegram client started")


if __name__ == "__main__":
  asyncio.run(main())