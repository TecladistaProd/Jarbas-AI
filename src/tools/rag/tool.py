from langchain_core.tools import create_retriever_tool
from loguru import logger

from .loader import load_documents
from .splitter import split_documents
from .vecstore import build_vectorstore


_vectorstore = None
_tool = None


def _get_vectorstore():
  global _vectorstore

  if _vectorstore is not None:
    return _vectorstore

  logger.info("Carregando documentos para RAG")
  docs = load_documents()

  if not docs:
    logger.error("Nenhum documento encontrado para o RAG")
    raise ValueError("Nenhum dado encontrado para o RAG.")

  logger.info("Dividindo documentos em chunks")
  chunks = split_documents(docs)
  logger.debug(f"{len(chunks)} chunks gerados")
  logger.info("Construindo vectorstore")
  _vectorstore = build_vectorstore(chunks)

  logger.success("Vectorstore criado (inicialização única)")

  return _vectorstore


def build_rag_tool():
  global _tool

  if _tool is not None:
    return _tool

  vectorstore = _get_vectorstore()

  logger.debug("Configurando retriever (k=3)")
  retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
  )

  _tool = create_retriever_tool(
    retriever,
    name="pesquisar_vida",
    description="Busca informações sobre o dono do sistema (currículo, experiências, habilidades)."
  )

  return _tool