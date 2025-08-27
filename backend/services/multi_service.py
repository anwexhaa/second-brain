# services/multi_service.py
from services.pinecone_services import query_pinecone
from services.local_embedding_service import get_local_embedding
from utils.qa import get_answer

SCORE_THRESHOLD = 0.0  # allow all results

def generate_queries(question: str) -> list[str]:
    return [
        question,
        f"What is the meaning of: {question}?",
        f"Explain: {question}",
        f"{question} in simple words"
    ]

def multi_query(question: str, namespace: str = "default") -> str:
    queries = generate_queries(question)
    all_matches = []

    for q in queries:
        emb = get_local_embedding(q)
        if emb:
            res = query_pinecone(emb, namespace=namespace)
            if res:
                all_matches.extend(res)

    # Deduplicate by match ID
    seen = set()
    deduped = []
    for match in all_matches:
        if match.id not in seen:
            seen.add(match.id)
            deduped.append(match)

    contexts = [
        m.metadata["text"]
        for m in deduped
        if hasattr(m, "metadata") and "text" in m.metadata
    ]

    # Debug printing contexts
    print(f"\n📎 Retrieved Contexts: {len(contexts)} found")
    for i, ctx in enumerate(contexts):
        print(f"#{i+1}: {ctx[:150]}...\n")

    context_str = "\n\n".join(contexts)
    return get_answer(question=question, context=context_str)
