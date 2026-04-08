import re
from markdown_it import MarkdownIt

md = MarkdownIt()
MAX_LEN = 2000

def smart_chunk_markdown(text: str, max_len: int = MAX_LEN):
  # 1. separa blocos principais (parágrafos/code blocks)
  blocks = re.split(r'(\n{2,}|```.*?```)', text, flags=re.DOTALL)

  chunks = []
  current = ""

  for block in blocks:
    if not block.strip():
      continue

    if len(block) > max_len:
      # fallback para tokenização leve
      words = re.findall(r'\S+\s*', block)

      temp = ""
      for w in words:
        if len(temp) + len(w) > max_len:
          chunks.append(temp)
          temp = ""
        temp += w

      if temp:
        chunks.append(temp)

      continue

    if len(current) + len(block) > max_len:
      if current:
        chunks.append(current)
        current = ""

    current += block

  if current:
    chunks.append(current)

  return chunks