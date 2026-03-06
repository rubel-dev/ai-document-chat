import pdfplumber
from fastapi import UploadFile

def extract_text_from_pdf(file:UploadFile):
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"
    return text.strip()

def chunk_text(text, chunk_size = 1000, overlap = 200):
    chunks = []

    start = 0
    step = chunk_size - overlap

    while start < len(text):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
        start += step
    return chunks

def ingest_pdf(file: UploadFile):
    text = extract_text_from_pdf(file)
    if not text:
        return []
    return chunk_text(text)