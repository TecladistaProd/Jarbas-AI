import asyncio
import random
import time

from telethon import TelegramClient, events
from telethon.tl.types import User
from telethon import functions
from loguru import logger

from langchain_core.messages import HumanMessage

from src.agent.graph import graph
from src.agent.state import INITIAL_TOOL_USAGE

from src.utils.md_tokenizing import smart_chunk_markdown


TRIGGER = "jarbas responde aqui"

MIN_DELAY = 1.5
MAX_DELAY = 4.0

# controle de flood por usuário
last_response_time = {}


class TelegramService:
  def __init__(self, api_id: int, api_hash: str, session_name: str = "jarbas_session"):
    self.client = TelegramClient(session_name, api_id, api_hash)

  def _build_initial_state(self, message: str):
    return {
      "message": message,  # 🔥 ESSENCIAL
      "messages": [HumanMessage(content=message)],
      "tool_usage": INITIAL_TOOL_USAGE.copy()
    }

  async def _human_delay(self, user_id: int):
    now = time.time()
    last_time = last_response_time.get(user_id, 0)

    delay = random.uniform(MIN_DELAY, MAX_DELAY)

    # evita flood sequencial
    if now - last_time < delay:
      await asyncio.sleep(delay)

    last_response_time[user_id] = time.time()

  async def start(self):
    # @self.client.on(events.NewMessage(incoming=True))
    @self.client.on(events.NewMessage)
    async def handler(event):
      if not event.is_private:
        return

      sender = await event.get_sender()

      if not isinstance(sender, User):
        return

      text_raw = event.raw_text
      text = text_raw.lower()

      is_trigger = TRIGGER in text

      logger.bind(user_id=sender.id).info(
        f"Mensagem de {sender.first_name}: {text_raw}"
      )

      # 🧠 CASO 1: você mesmo → só responde com trigger
      if sender.is_self:
        if not is_trigger:
          return

      # 🧠 CASO 2: outra pessoa → responde normalmente
      else:
        if not text.strip():
          return

      try:
        user_id = sender.id

        # 🔥 opcional: limpar trigger
        clean_text = text_raw.replace(TRIGGER, "").strip()

        state = self._build_initial_state(clean_text)

        logger.debug(f"Invocando agent para user_id={user_id}")
        result = graph.invoke(
          state,
          config={"configurable": {"thread_id": user_id}}
        )
        logger.debug("Resposta gerada com sucesso")

        response_text = result["messages"][-1].content

        await self._human_delay(user_id)

        async with self.client.action(event.chat_id, "typing"):
          await asyncio.sleep(random.uniform(0.5, 1.5))

        await event.reply(response_text, parse_mode="md")
        # chunks = smart_chunk_markdown(response_text, 2000)

        # for chunk in chunks:
        #   await event.reply(chunk, parse_mode="markdown")
        #   if len(chunks) > 1:
        #     await asyncio.sleep(1)

      except Exception as e:
        logger.exception("Erro ao processar mensagem")
        await event.reply("Erro interno do JARBAS.")

    logger.info("JARBAS conectado ao Telegram...")
    await self.client.start()
    await self.client.run_until_disconnected()