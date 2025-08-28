from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os, shutil, tempfile
import pdfplumber
import fitz  # PyMuPDF

from utils.chunk_text import get_text_chunks
from utils.embed import embed_texts, upsert_to_pinecone

router = APIRouter()

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...), namespace: str = Form("default")):
    try:
        suffix = os.path.splitext(file.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_file_path = tmp.name

        text = ""
        try:
            with pdfplumber.open(temp_file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except:
            text = ""

        if not text.strip():
            try:
                with fitz.open(temp_file_path) as doc:
                    text = "\n".join([page.get_text() for page in doc])
            except:
                raise HTTPException(status_code=400, detail="Could not extract text")

        os.remove(temp_file_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted")

        chunks = get_text_chunks(text)
        if not chunks:
            raise HTTPException(status_code=500, detail="Text chunking failed")

        metadata_list = [{
            "source": file.filename,
            "chunk_index": i,
            "original_length": len(chunk),
            "text": chunk
        } for i, chunk in enumerate(chunks)]

        vectors = embed_texts(chunks, metadata_list)
        if not vectors:
            raise HTTPException(status_code=500, detail="Embedding generation failed")

        upsert_to_pinecone(vectors, namespace)

        return {"message": f"File processed and upserted {len(vectors)} chunks.", "chunks": len(vectors)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
