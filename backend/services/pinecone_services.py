from pinecone import Pinecone
import config

# Initialize Pinecone client & index
pc = Pinecone(api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)


def query_pinecone(query_embedding: list[float], top_k: int = 5, namespace: str = "default"):
    """
    Query Pinecone for the most relevant vectors given an embedding.
    """
    try:
        response = index.query(
            vector=query_embedding,
            top_k=int(top_k),
            include_metadata=True,
            namespace=namespace
        )
        return response.to_dict()  # ✅ Always return a dictionary with "matches"
    except Exception as e:
        print(f"❌ Error querying Pinecone: {e}")
        return {"matches": []}
