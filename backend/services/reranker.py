# backend/services/reranker.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def calculate_relevance_score(query: str, document_text: str) -> float:
    """
    Use Gemini to score relevance between query and document.
    Returns a score between 0 and 1.
    """
    prompt = f"""
    Rate the relevance of this document to the query on a scale of 0.0 to 1.0, where:
    - 1.0 = highly relevant, directly answers the query
    - 0.5 = somewhat relevant, contains related information
    - 0.0 = not relevant at all
    
    Query: {query}
    Document: {document_text}
    
    Respond with only a number between 0.0 and 1.0.
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        score = float(response.text.strip())
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, score))
    except Exception as e:
        print(f"Error calculating relevance score: {e}")
        # Fallback: return neutral score
        return 0.5

def rerank_results(query: str, docs: list):
    """
    Rerank documents based on relevance to query using Gemini.
    """
    for doc in docs:
        document_text = doc.metadata.get("text", "")
        doc.rerank_score = calculate_relevance_score(query, document_text)
    
    return sorted(docs, key=lambda x: x.rerank_score, reverse=True)