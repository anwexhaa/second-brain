# services/rag_fusion_services.py
from services.pinecone_services import query_pinecone
from services.openai_services import get_embedding, generate_hypothetical_answer
from services.query_decomposition import decompose_question

SCORE_THRESHOLD = 0.0
TOP_K = 5

# Map user intents to keywords for filtering context
KEYWORD_MAP = {
    "overview": ["overview", "summary", "introduction", "about", "purpose"],
    "goal": ["goal", "objective", "aim", "target"],
    "architecture": ["architecture", "design", "structure", "components"],
    "features": ["feature", "capability", "functionality"],
    "usage": ["usage", "how to use", "instructions", "steps"],
    "security": ["security", "privacy", "compliance", "regulation"],
    # add more mappings as needed
}

def filter_context_by_keywords(contexts: list[str], question: str) -> list[str]:
    question_lower = question.lower()
    keywords = []
    for key, kw_list in KEYWORD_MAP.items():
        if key in question_lower:
            keywords = kw_list
            break
    if not keywords:
        return contexts  # fallback: use all context if no keyword match

    filtered = [c for c in contexts if any(kw in c.lower() for kw in keywords)]
    return filtered or contexts  # fallback if filtering yields nothing

def rag_fusion(question: str, namespace: str = "default") -> str:
    sub_questions = decompose_question(question)
    print("🧠 Sub-questions:", sub_questions)

    all_matches = []

    # Step 1: Search Pinecone for each sub-question
    for sub_q in sub_questions:
        embedding = get_embedding(sub_q)
        if embedding:
            response = query_pinecone(embedding, namespace=namespace)
            if response:
                all_matches.extend(response)

    # Step 2: Deduplicate results by ID
    seen = set()
    deduped = []
    for match in all_matches:
        if match.id not in seen:
            seen.add(match.id)
            deduped.append(match)

    # Step 3: Score filtering (optional)
    filtered = [m for m in deduped if getattr(m, "score", 0) >= SCORE_THRESHOLD]
    if not filtered:
        return "I don't have information on that."

    # Step 4: Take top-k results directly
    top_k = filtered[:TOP_K]

    # Step 5: Prepare context for answer generation
    contexts = [
        m.metadata.get("text", "")
        for m in top_k
        if hasattr(m, "metadata") and "text" in m.metadata
    ]

    if not contexts:
        return "I don't have information on that."

    # Step 6: Filter context by question keywords
    contexts = filter_context_by_keywords(contexts, question)
    combined_context = "\n\n".join(contexts)
    print("📚 Filtered Context:\n", combined_context)

    # Step 7: Strict prompt to avoid hallucination
    prompt = f"""
You are Nova, a friendly and human-like AI assistant. Answer the user's question **using ONLY the text in the context below**.
Do NOT add any information that is not present in the context.
If the answer is not in the context, respond exactly: "I don't have information on that."
Keep answers concise (1-2 sentences), and use emojis sparingly if it helps friendliness.

Context:
{combined_context}

User Question: {question}
Nova:"""

    return generate_hypothetical_answer(prompt)
