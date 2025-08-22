from services.pinecone_services import query_pinecone
from services.openai_services import get_embedding, get_answer

def decompose_question(question: str) -> list[str]:
    if ' and ' in question.lower():
        parts = [q.strip() for q in question.split(' and ')]
    else:
        parts = [question]
    return parts

def query_decomposition(question: str, namespace: str = "default") -> str:
    sub_questions = decompose_question(question)
    all_contexts = []

    for sub_q in sub_questions:
        emb = get_embedding(sub_q)
        if not emb:
            continue
        res = query_pinecone(emb, namespace=namespace)
        if not res:
            continue

        contexts = [
            match.metadata.get('text', '')
            for match in res
            if hasattr(match, "metadata") and 'text' in match.metadata
        ]
        all_contexts.extend(contexts)

    if not all_contexts:
        return "Sorry, no relevant information found to answer this."

    context_str = "\n\n".join(all_contexts)
    final_prompt = f"Answer the question based on the context below:\n\nContext:\n{context_str}\n\nQuestion: {question}"

    return get_answer(question=question, context=context_str)
