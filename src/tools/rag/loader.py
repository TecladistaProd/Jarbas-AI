import time
from src.data_processing import process_pdf, BASE_DIR, OUTPUT_PATH

EXTRA_PATH = BASE_DIR / "data" / "extra.md"

def load_resume():
  if OUTPUT_PATH.exists():
    return OUTPUT_PATH.read_text(encoding="utf-8")

def load_documents():
  data = []

  resume_data = load_resume()
  if resume_data:
    data.append(resume_data)
  else:
    process_pdf()
    time.sleep(2)
    resume_data = load_resume()
    if resume_data:
      data.append(resume_data)

  if EXTRA_PATH.exists():
    data.append(EXTRA_PATH.read_text(encoding="utf-8"))

  return data