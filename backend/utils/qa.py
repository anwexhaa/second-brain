# utils/qa.py
from transformers import pipeline

qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def get_answer(question: str, context: str) -> str:
    result = qa_model(question=question, context=context)
    return result["answer"]
