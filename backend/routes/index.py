from fastapi import APIRouter, Body
from typing import Optional
from services.indexing_service import index_text_to_pinecone  # update path if different

router = APIRouter()

@router.post("/")
def index_text(
    text: str = Body(...),
    namespace: Optional[str] = Body("default")
):
    return index_text_to_pinecone(text, namespace)
