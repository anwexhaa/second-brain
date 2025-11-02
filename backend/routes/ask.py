from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

# import text store from upload route
from routes.upload import uploaded_texts

# Load env & setup Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    namespace: str = "default"

@router.post("/")
async def ask_question(payload: QueryRequest):
    """
    Handles user questions or follow-ups about uploaded PDFs or text.
    Uses Gemini 2.0 Flash directly with stored document context.
    """
    try:
        question = payload.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Please provide a question or text to summarize.")

        # retrieve context if available
        context = uploaded_texts.get(payload.namespace, "")
        if context:
            prompt = f"Context:\n{context}\n\nQuestion: {question}"
        else:
            prompt = question  # fallback if no uploaded file yet

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        answer = response.text.strip() if response and response.text else "No answer generated."

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini request failed: {str(e)}")
