from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os, shutil, tempfile
import pdfplumber
import fitz  # PyMuPDF
from dotenv import load_dotenv
import google.generativeai as genai

from utils.chunk_text import get_text_chunks  # still useful for clean input

# Load .env and setup Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...), namespace: str = Form("default")):
    """
    Uploads a PDF, extracts its text, summarizes it using Gemini 2.0 Flash, 
    and returns the summary (no embeddings or Pinecone).
    """
    try:
        # Save uploaded file temporarily
        suffix = os.path.splitext(file.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_file_path = tmp.name

        # Extract text with pdfplumber first
        text = ""
        try:
            with pdfplumber.open(temp_file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception:
            text = ""

        # If still empty, fallback to PyMuPDF
        if not text.strip():
            try:
                with fitz.open(temp_file_path) as doc:
                    text = "\n".join([page.get_text() for page in doc])
            except Exception:
                raise HTTPException(status_code=400, detail="Could not extract text")

        os.remove(temp_file_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from file")

        # Optional: chunk text if very long (prevents hitting token limits)
        chunks = get_text_chunks(text)
        limited_text = "\n\n".join(chunks[:5])  # summarize first few chunks if huge

        # --- Use Gemini Flash for summarization ---
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Summarize the following document in detail:\n\n{limited_text}"
        response = model.generate_content(prompt)

        summary = response.text.strip() if response and response.text else "No summary generated."

        return {
            "message": f"File processed successfully: {file.filename}",
            "summary": summary,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
