# utils/qa.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_answer(question: str, context: str) -> str:
    if not question or not context:
        return ""
    prompt = f"Answer the question based on the context:\n\nContext:\n{context}\n\nQuestion:\n{question}\nAnswer:"
    try:
        response = genai.generate_text(
            model="models/text-bison-001",
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=200
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating answer: {e}")
        return ""
