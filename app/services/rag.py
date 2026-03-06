import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")

def rag_answer(question, docs):

    context = "\n\n".join(doc.page_content for doc in docs)
    prompt = f"""
Context:
{context}

Question:
{question}
answer using only the context.
"""
    
    llm = ChatGoogleGenerativeAI(
        model = LLM_MODEL,
        temparature=0
    )

    response = llm.invoke(prompt)
    return response.content
