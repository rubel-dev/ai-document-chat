# app/main.py

from fastapi import FastAPI, UploadFile, File
from app.services.ingest import ingest_pdf
from app.services.vectorstore import add_documents, search_documents
from pydantic import BaseModel
from app.services.rag import rag_answer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app = FastAPI()


class ChatRequest(BaseModel):
    question: str

app.mount("/static", StaticFiles(directory='app/static'), name = 'static')
@app.get("/")
async def root():
    return FileResponse("app/static/index.html")
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    chunks = ingest_pdf(file)
    add_documents(chunks)

    return {
        "filename": file.filename,
        "chunk_count": len(chunks),
        "stored": True
    }

@app.post('/chat')
async def chat(data: ChatRequest):
    docs = search_documents(data.question)
    answer = rag_answer(data.question, docs)
    return {"answer": answer}
