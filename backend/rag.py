from services.openai_services import get_embedding
from services.pinecone_services import query_pinecone

def build_context(question: str, namespace: str, top_k: int = 5) -> str:
    query_embedding = get_embedding(question)
    results = query_pinecone(query_embedding, namespace=namespace, top_k=top_k)

    if not results or "matches" not in results:
        return ""

    context_chunks = []
    for match in results["matches"]:
        metadata = match.get("metadata")
        if isinstance(metadata, dict) and "text" in metadata:
            context_chunks.append(metadata["text"])
        else:
            print("⚠️ Invalid or missing 'text' in metadata:", metadata)

    return "\n\n".join(context_chunks)


# Optional test
if __name__ == "__main__":
    question = "What is the main idea of the notes?"
    namespace = "test-namespace"
    context = build_context(question, namespace)
    print("Context built:\n", context)
