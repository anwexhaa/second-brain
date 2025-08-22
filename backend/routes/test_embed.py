# routes/test_embed.py

from fastapi import APIRouter
from utils.pinecone_utils import upsert_to_pinecone
from utils.embed import embed_texts

router = APIRouter()

@router.get("/test-upsert")
def test_upsert():
    texts = [
        "Einstein proposed the theory of relativity.",
        "Python is a powerful programming language."
    ]

    metadata_list = [
        {"source": "science_notes.txt", "chunk": 0, "text": texts[0]},
        {"source": "programming_notes.txt", "chunk": 1, "text": texts[1]}
    ]

    vectors = embed_texts(texts, metadata_list)
    if vectors:
        upsert_to_pinecone(vectors, namespace="test")
        return {"message": f"✅ Upserted {len(vectors)} vectors to Pinecone."}
    else:
        return {"message": "❌ Embedding failed"}
