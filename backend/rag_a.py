from services.openai_services import get_answer, get_embedding
from services.pinecone_services import query_pinecone

# Map common keywords to boost retrieval relevance
KEYWORD_SYNONYMS = {
    "overview": ["overview", "summary", "introduction", "high-level", "about", "purpose"],
    "features": ["features", "capabilities", "functionalities"],
    "architecture": ["architecture", "design", "structure", "workflow", "lifecycle"],
    "technical": ["technical", "implementation", "details", "specs", "mechanisms"],
}

def map_keywords(question: str):
    q_lower = question.lower()
    for key, synonyms in KEYWORD_SYNONYMS.items():
        for syn in synonyms:
            if syn in q_lower:
                return key
    return None

def answer_question(question: str, namespace: str, top_k: int = 5, relevance_threshold: float = 0.5):
    """
    Returns an answer to the question using Pinecone retrieval and Gemini LLM.
    relevance_threshold: minimum Pinecone score to include a snippet in context
    """
    # Step 0: Keyword mapping
    keyword = map_keywords(question)
    question_for_ai = f"Provide a clear {keyword} from the document." if keyword else question

    # Step 1: Get embedding
    embedding = get_embedding(question_for_ai)

    # Step 2: Query Pinecone
    pinecone_results = query_pinecone(embedding, namespace=namespace, top_k=top_k) or {}
    matches = pinecone_results.get("matches", [])

    # Step 3: Filter relevant texts for LLM context
    relevant_texts = []
    for m in matches:
        text = m.get("metadata", {}).get("text", "")
        score = m.get("score", 0)
        # Include if keyword matches or score is above threshold
        if keyword and (keyword in text.lower() or any(syn in text.lower() for syn in KEYWORD_SYNONYMS[keyword])):
            relevant_texts.append(text)
        elif score >= relevance_threshold:
            relevant_texts.append(text)

    # Step 4: Generate answer
    if relevant_texts:
        final_answer = get_answer(question_for_ai, "\n\n".join(relevant_texts))
    else:
        # purely conversational fallback
        final_answer = get_answer(question, "")

    # Step 5: Format matches for frontend (even if empty)
    formatted_matches = [
        {
            "text": m.get("metadata", {}).get("text", ""),
            "score": m.get("score", 0),
            "source": m.get("metadata", {}).get("source", "unknown")
        }
        for m in matches
    ]

    return {"answer": final_answer, "matches": formatted_matches}
