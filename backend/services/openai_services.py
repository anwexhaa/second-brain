import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (for GEMINI_API_KEY)
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

# Use Gemini for LLM generation
gemini_model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"

def generate_hypothetical_answer(prompt: str) -> str:
    try:
        print("[LLM: Gemini] Generating response...")  # 👈 log which LLM is being used
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Error generating hypothetical answer with Gemini: {e}")
        return ""

# Wrapper function to add context to the question
def get_answer(question: str, context: str) -> str:
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    return generate_hypothetical_answer(prompt)

# Test
if __name__ == "__main__":
    long_context = " ".join(["Knowledge graphs are structured representations of facts."] * 100)
    print(get_answer("How do knowledge graphs help in RAG?", long_context))