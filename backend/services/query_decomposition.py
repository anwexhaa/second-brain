# services/query_decomposition.py

def decompose_question(question: str) -> list[str]:
    """
    Simple heuristic to break down a complex question into sub-questions.
    Splits on common conjunctions like 'and', 'or', 'but'.
    """
    import re
    parts = re.split(r"\band\b|\bor\b|\bbut\b", question, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]
