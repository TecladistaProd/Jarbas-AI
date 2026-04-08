from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def build_vectorstore(chunks):
  embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
  )

  vectorstore = FAISS.from_texts(
    chunks,
    embeddings,
    metadatas=[{"source": "local"} for _ in chunks]
  )

  return vectorstore