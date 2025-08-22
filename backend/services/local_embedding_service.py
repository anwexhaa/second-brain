# services/local_embedding_service.py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_local_embedding(text: str):
    if not text:
        return None
    return model.encode(text, convert_to_numpy=True).tolist()
