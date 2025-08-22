# backend/services/reranker.py
from sentence_transformers import CrossEncoder

# Load the pretrained MiniLM reranker
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_results(query: str, docs: list):
    pairs = [(query, doc.metadata.get("text", "")) for doc in docs]
    scores = reranker.predict(pairs)
    for doc, score in zip(docs, scores):
        doc.rerank_score = score
    return sorted(docs, key=lambda x: x.rerank_score, reverse=True)
