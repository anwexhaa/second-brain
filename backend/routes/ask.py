from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load env & setup Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    namespace: str = "default"  # keep for compatibility

@router.post("/")
async def ask_question(payload: QueryRequest):
    """
    Direct Gemini 2.0 Flash chat/summary endpoint.
    No Pinecone or RAG retrieval — just pure LLM response.
    """
    try:
        question = payload.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Please provide a question or text to summarize.")

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(question)
        answer = response.text.strip() if response and response.text else "No answer generated."

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini request failed: {str(e)}")
