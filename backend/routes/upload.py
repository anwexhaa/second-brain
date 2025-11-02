from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os, shutil, tempfile
import pdfplumber
import fitz  # PyMuPDF
from dotenv import load_dotenv
import google.generativeai as genai
from utils.chunk_text import get_text_chunks

# Load .env and setup Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

# simple in-memory text store (namespace → text)
uploaded_texts = {}

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...), namespace: str = Form("default")):
    """
    Upload a PDF, extract its text, store it for later queries,
    and return an immediate summary using Gemini 2.0 Flash.
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

        # Fallback to PyMuPDF if pdfplumber fails
        if not text.strip():
            try:
                with fitz.open(temp_file_path) as doc:
                    text = "\n".join([page.get_text() for page in doc])
            except Exception:
                raise HTTPException(status_code=400, detail="Could not extract text")

        os.remove(temp_file_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from file")

        # store extracted text in memory (for later queries)
        uploaded_texts[namespace] = text

        # Chunk + summarize part of it for immediate feedback
        chunks = get_text_chunks(text)
        limited_text = "\n\n".join(chunks[:5])  # summarize only first few chunks

        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Summarize the following document clearly and concisely:\n\n{limited_text}"
        response = model.generate_content(prompt)
        summary = response.text.strip() if response and response.text else "No summary generated."

        return {
            "message": f"File processed and stored successfully: {file.filename}",
            "namespace": namespace,
            "summary": summary,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
