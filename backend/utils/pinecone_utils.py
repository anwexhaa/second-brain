from pinecone import Pinecone
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

def get_or_create_index(dimension: int):
    indexes = pc.list_indexes()
    if PINECONE_INDEX_NAME not in [index['name'] for index in indexes]:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=dimension,
            metric="cosine"
        )
    return pc.Index(PINECONE_INDEX_NAME)

def upsert_to_pinecone(vectors: List[Dict[str, Any]], namespace:str) -> None:
    try:
        index = pc.Index(PINECONE_INDEX_NAME)
        index.upsert(vectors=vectors, namespace=namespace)
        print(f"✅ Upserted {len(vectors)} vectors to Pinecone.")
    except Exception as e:
        print(f"❌ [upsert_to_pinecone] Error: {e}")
