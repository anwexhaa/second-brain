# services/local_llm_service.py
from transformers import pipeline

qa_pipeline = pipeline("text-generation", model="tiiuae/falcon-rw-1b", tokenizer="tiiuae/falcon-rw-1b")

def get_local_answer(question: str, context: str):
    prompt = f"Answer the question based on the context:\n\nContext:\n{context}\n\nQuestion:\n{question}\nAnswer:"
    result = qa_pipeline(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
    return result[0]["generated_text"].replace(prompt, "").strip()
