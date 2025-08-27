import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from pinecone import Pinecone
import config

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Same Pinecone client + index as query side
pc = Pinecone(api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)

def generate_embedding(text: str) -> List[float]:
    """Generate embedding for a single text using Gemini."""
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding for text: {e}")
        return []

def embed_texts(texts: List[str], metadata_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate embeddings for a list of texts and package them with metadata for Pinecone upsert.
    """
    vectors = []
    print(f"Generating embeddings for {len(texts)} texts...")
    
    for i, (text, meta) in enumerate(zip(texts, metadata_list)):
        embedding = generate_embedding(text)
        if embedding:  # Only add if embedding generation was successful
            vectors.append({
                "id": f"chunk-{i}",
                "values": embedding,
                "metadata": meta
            })
        
        # Show progress
        if (i + 1) % 10 == 0 or (i + 1) == len(texts):
            print(f"Processed {i + 1}/{len(texts)} texts")
    
    return vectors

def upsert_to_pinecone(vectors: List[Dict[str, Any]], namespace: str = "default"):
    """
    Upsert a list of vectors into Pinecone under a given namespace.
    """
    try:
        index.upsert(vectors=vectors, namespace=namespace)
        print(f"✅ Upserted {len(vectors)} vectors to Pinecone (namespace: {namespace})")
    except Exception as e:
        print(f"❌ Error during upsert: {e}")

# ---------- Example usage ----------
if __name__ == "__main__":
    sample_texts = [
        "The mitochondria is the powerhouse of the cell.",
        "FastAPI is a modern, fast web framework for Python."
    ]
    sample_metadata = [
        {"source": "bio_notes.txt"},
        {"source": "dev_notes.txt"}
    ]

    vectors = embed_texts(sample_texts, sample_metadata)
    if vectors:
        upsert_to_pinecone(vectors)