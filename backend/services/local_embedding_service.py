# services/local_embedding_service.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_local_embedding(text: str):
    if not text:
        return None
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None