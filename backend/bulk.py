# bulk_index.py
from services.openai_services import get_embedding
from services.pinecone_services import pc, index  # assuming pc and index are exposed
import os

docs = [
    "Pinecone is a vector database used for similarity search and semantic retrieval.",
    "FastAPI is a modern, fast web framework for building APIs with Python 3.6+.",
    "OpenAI provides powerful models for NLP and embeddings.",
    "RAG (Retrieval-Augmented Generation) combines retrieval and generation for better QA.",
    "HyDE (Hypothetical Document Embeddings) improves generation quality with synthetic contexts."
]

def bulk_index(docs, namespace="default"):
    to_upsert = []
    for i, doc in enumerate(docs):
        vec = get_embedding(doc)
        to_upsert.append({
            "id": f"doc-{i}",
            "values": vec,
            "metadata": {"text": doc}
        })

    index.upsert(to_upsert, namespace=namespace)
    print(f"✅ Indexed {len(docs)} documents.")

if __name__ == "__main__":
    bulk_index(docs)
