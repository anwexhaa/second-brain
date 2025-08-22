# manual.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from services.openai_services import get_embedding

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Check if .env values are loaded
if not PINECONE_API_KEY or not PINECONE_INDEX_NAME:
    raise ValueError("❌ Pinecone API key or index name not loaded from .env!")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Dummy text to embed and index
dummy_text = "Pinecone is a vector database used for similarity search and semantic retrieval."
vector = get_embedding(dummy_text)

# Upsert into Pinecone
index.upsert([
    {
        "id": "pinecone-doc",
        "values": vector,
        "metadata": {"text": dummy_text}
    }
], namespace="default")

print("✅ Dummy document indexed to Pinecone!")
