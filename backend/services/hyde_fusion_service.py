from services.pinecone_services import query_pinecone
from services.openai_services import get_embedding, get_answer, generate_hypothetical_answer
from services.query_decomposition_service import decompose_question

SCORE_THRESHOLD = 0.0

def hyde_fusion(question: str, namespace: str = "default") -> str:
    # Step 1: Decompose question into sub-questions
    sub_questions = decompose_question(question)
    all_matches = []

    # Step 2: Generate hypothetical answers (HyDE) for each sub-question and embed them
    for sub_q in sub_questions:
        hypothetical_answer = generate_hypothetical_answer(sub_q)
        if hypothetical_answer:
            hyde_embedding = get_embedding(hypothetical_answer)
            if hyde_embedding:
                hyde_results = query_pinecone(hyde_embedding, namespace=namespace)
                if hyde_results:
                    all_matches.extend(hyde_results)

    # Step 3: Also retrieve matches for original sub-questions (RAG fusion)
    for sub_q in sub_questions:
        emb = get_embedding(sub_q)
        if emb:
            rag_results = query_pinecone(emb, namespace=namespace)
            if rag_results:
                all_matches.extend(rag_results)

    # Deduplicate matches by ID
    seen = set()
    deduped = []
    for match in all_matches:
        if match.id not in seen:
            seen.add(match.id)
            deduped.append(match)

    # Filter by score threshold
    filtered = [m for m in deduped if getattr(m, "score", 0) >= SCORE_THRESHOLD]

    contexts = [
        m.metadata.get("text", "")
        for m in filtered
        if hasattr(m, "metadata") and "text" in m.metadata
    ]

    if not contexts:
        return "Sorry, no relevant information found to answer this."

    context_str = "\n\n".join(contexts)
    final_prompt = f"Answer the question based on the context below:\n\nContext:\n{context_str}\n\nQuestion: {question}"

    # Generate the final answer from combined contexts
    return get_answer(question=question, context=context_str)
