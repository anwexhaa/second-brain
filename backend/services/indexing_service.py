import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from services.openai_services import get_embedding
from utils.pinecone_utils import upsert_to_pinecone
from utils.chunk_text import get_text_chunks
from uuid import uuid4

def index_text_to_pinecone(text:str, namespace:str="default"):
    chunks = get_text_chunks(text)
    vectors = []

    for chunk in chunks:
        embedding = get_embedding(chunk)
        if embedding:
            vectors.append({
                "id": str(uuid4()),
                "values": embedding,
                "metadata": {"text": chunk}
            })
    upsert_to_pinecone(vectors,namespace)
    return {"message": f"Indexed {len(vectors)} chunks into Pinecone"}


#checking
if __name__ == "__main__":
    import sys
    sys.path.append("..")  # so it can find `utils`, `services`, etc.

    sample_text = """
    Pinecone is a vector database that lets you store, search, and retrieve high-dimensional vector representations of data.
    It's commonly used with embeddings generated from models like OpenAI or SentenceTransformers in AI applications.
    """
    response = index_text_to_pinecone(sample_text, namespace="default")
    print(response)

