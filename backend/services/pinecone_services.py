# from pinecone import Pinecone
# import config

# # Initialize Pinecone client & index
# pc = Pinecone(api_key=config.PINECONE_API_KEY)
# index = pc.Index(config.PINECONE_INDEX_NAME)


# def query_pinecone(query_embedding: list[float], top_k: int = 5, namespace: str = "default"):
#     """
#     Query Pinecone for the most relevant vectors given an embedding.
#     """
#     try:
#         response = index.query(
#             vector=query_embedding,
#             top_k=int(top_k),
#             include_metadata=True,
#             namespace=namespace
#         )
#         return response.to_dict()  # ✅ Always return a dictionary with "matches"
#     except Exception as e:
#         print(f"❌ Error querying Pinecone: {e}")
#         return {"matches": []}

from pinecone import Pinecone
import config
import uuid

# ✅ Generate a unique namespace per session/chat
SESSION_NAMESPACE = str(uuid.uuid4())

# Initialize Pinecone client & index
pc = Pinecone(api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)


def upload_pdf_vectors(vectors: list[dict]):
    """
    Upsert new PDF vectors into Pinecone.
    Clears any previous vectors in this session first.
    vectors = [{"id": "chunk1", "values": embedding, "metadata": {"text": "..."}}]
    """
    try:
        # Clear previous PDF vectors in this session
        index.delete(delete_all=True, namespace=SESSION_NAMESPACE)
        # Insert new vectors
        index.upsert(vectors=vectors, namespace=SESSION_NAMESPACE)
        print(f"✅ Uploaded {len(vectors)} vectors to session namespace {SESSION_NAMESPACE}")
    except Exception as e:
        print(f"❌ Error uploading vectors: {e}")


def query_pinecone(query_embedding: list[float], top_k: int = 5):
    """
    Query Pinecone for the most relevant vectors given an embedding.
    Only searches within the current session namespace.
    """
    try:
        response = index.query(
            vector=query_embedding,
            top_k=int(top_k),
            include_metadata=True,
            namespace=SESSION_NAMESPACE
        )
        return response.to_dict()  # ✅ Always return a dictionary with "matches"
    except Exception as e:
        print(f"❌ Error querying Pinecone: {e}")
        return {"matches": []}
