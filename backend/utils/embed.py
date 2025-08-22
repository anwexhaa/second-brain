from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from pinecone import Pinecone
import config

# Use the same embedding model everywhere
model = SentenceTransformer("all-MiniLM-L6-v2")

# Same Pinecone client + index as query side
pc = Pinecone(api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)


def embed_texts(texts: List[str], metadata_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate embeddings for a list of texts and package them with metadata for Pinecone upsert.
    """
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True).tolist()
    return [
        {"id": f"chunk-{i}", "values": emb, "metadata": meta}
        for i, (emb, meta) in enumerate(zip(embeddings, metadata_list))
    ]


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
