from langchain_text_splitters import MarkdownTextSplitter


def split_documents(docs):
  splitter = MarkdownTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    strip_whitespace=True
  )

  chunks = []

  for doc in docs:
    parts = splitter.split_text(doc)
    chunks.extend([p.strip() for p in parts if p.strip()])

  return chunks