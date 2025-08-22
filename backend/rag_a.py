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

def answer_question(question: str, namespace: str, top_k: int = 5):
    # Step 0: Keyword mapping
    keyword = map_keywords(question)
    question_for_ai = f"Provide a clear {keyword} from the document." if keyword else question

    # Step 1: Get embedding
    embedding = get_embedding(question_for_ai)

    # Step 2: Query Pinecone
    pinecone_results = query_pinecone(embedding, namespace=namespace, top_k=top_k) or {}
    matches = pinecone_results.get("matches", [])

    # Step 3: Extract texts
    texts = [m.get("metadata", {}).get("text", "") for m in matches if m.get("metadata", {}).get("text")]

    if not texts:
        return {"answer": "❌ Sorry, I couldn't find any relevant information.", "matches": []}

    # --- Step 4: Return exact retrieved snippet if keyword exists ---
    if keyword:
        for text in texts:
            if keyword in text.lower() or any(syn in text.lower() for syn in KEYWORD_SYNONYMS[keyword]):
                return {
                    "answer": text.strip(),
                    "matches": [
                        {
                            "text": text.strip(),
                            "score": m.get("score", 0),
                            "source": m.get("metadata", {}).get("source", "unknown")
                        }
                        for m in matches
                        if m.get("metadata", {}).get("text") == text
                    ]
                }

    # Step 5: Only generate with get_answer() if NO relevant snippet is found
    final_answer = get_answer(question_for_ai, "\n\n".join(texts))

    # Step 6: Format matches for frontend
    formatted_matches = [
        {
            "text": m.get("metadata", {}).get("text", ""),
            "score": m.get("score", 0),
            "source": m.get("metadata", {}).get("source", "unknown")
        }
        for m in matches
    ]

    return {"answer": final_answer, "matches": formatted_matches}
