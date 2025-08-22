# filename: temp_index.py
from services.openai_services import get_embedding
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ load from env
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")

# ✅ no hardcoded values
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

dummy_text = "Pinecone is a vector database used for similarity search and semantic retrieval."

vector = get_embedding(dummy_text)

index.upsert([
    {"id": "pinecone-doc", "values": vector, "metadata": {"text": dummy_text}}
], namespace="default")

print("✅ Dummy document indexed.")
