from pathlib import Path
import pymupdf
from loguru import logger

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.utils import setup_llm, LLM_MODEL

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "data" / "resume.pdf"
OUTPUT_PATH = BASE_DIR / "data" / "resume.md"

PROMPT = """
Você irá estruturar um currículo em Markdown.

Regras:
- Organize em seções com headings (#, ##)
- Traduza o conteúdo para português, mas preserve termos técnicos que realmente sejam necessários e que não hajam em português ou pouco usual
- Resuma e compacte o que for necessário
- Compreenda que o processamento e separação deve ser focando em uso futuros em embeddings e RAG para agents
- Separe claramente:
  - Experiência
  - Skills
  - Educação
  - Projetos
  - Verifique se há skills ocultas no texto pelo contexto dos projetos, educação e experiências
  - Separe um campo para soft skills, caso haja mas valide se elas também não estão ocultas ou intrínsecas em outras seções
  - Use listas quando fizer sentido
- NÃO invente informações
- NÃO resuma demais, caso seja algo que possa perder contexto e relevância para RAG
- Preserve conteúdo relevante para busca semântica (RAG)
- Ignore informações irrelevantes para um currículo, como hobbies, a menos que sejam altamente relevantes para a posição desejada, ou mesmo textos e emojis que não sejam necessários para o RAG
- APENAS RESPONDA COM O MARKDOWN, SEM EXPLICAÇÕES E COM O TEXTO FORA DO BLOCO DE CÓDIGOS
- Use ZERO EMOJIS.

Texto:
{input}
"""


def extract_pdf_text():
  logger.info(f"Extraindo texto do PDF: {PDF_PATH}")
  doc = pymupdf.open(PDF_PATH)
  pages = [page.get_text() for page in doc]
  logger.debug(f"{len(pages)} páginas extraídas do PDF")
  return "\n".join(pages)


def process_pdf():
  logger.info("Iniciando processamento do currículo")
  raw_text = extract_pdf_text()
  logger.debug(f"Tamanho do texto extraído: {len(raw_text)} caracteres")

  model = LLM_MODEL.DEEPSEEK_REASONER
  logger.info(f"Usando modelo: {model}")
  llm = setup_llm(
    model=model,
    temperature=0.3
  )

  prompt = ChatPromptTemplate.from_template(PROMPT)

  chain = prompt | llm | StrOutputParser()

  markdown = chain.invoke({"input": raw_text})

  OUTPUT_PATH.write_text(markdown, encoding="utf-8")
  logger.success(f"Markdown salvo em: {OUTPUT_PATH}")

  return markdown