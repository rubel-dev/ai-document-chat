# app/services/vectorstore.py

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
print("DEBUG EMBED_MODEL =", os.getenv("EMBED_MODEL"))
print("DEBUG CHROMA_DIR =", os.getenv("CHROMA_DIR"))

CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/chroma")
EMBED_MODEL = os.getenv("EMBED_MODEL", "models/embedding-001")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_vectorstore():
    embedding_function = GoogleGenerativeAIEmbeddings(
        model=EMBED_MODEL,
        google_api_key=GEMINI_API_KEY
    )

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_function
    )

    return vectorstore


def add_documents(chunks: list[str]):
    if not chunks:
        return

    vectorstore = get_vectorstore()
    vectorstore.add_texts(chunks)


def search_documents(query: str, k: int = 3):
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    return results