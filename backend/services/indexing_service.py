# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



# from services.openai_services import get_embedding
# from utils.pinecone_utils import upsert_to_pinecone
# from utils.chunk_text import get_text_chunks
# from uuid import uuid4

# def index_text_to_pinecone(text:str, namespace:str="default"):
#     chunks = get_text_chunks(text)
#     vectors = []

#     for chunk in chunks:
#         embedding = get_embedding(chunk)
#         if embedding:
#             vectors.append({
#                 "id": str(uuid4()),
#                 "values": embedding,
#                 "metadata": {"text": chunk}
#             })
#     upsert_to_pinecone(vectors,namespace)
#     return {"message": f"Indexed {len(vectors)} chunks into Pinecone"}


# #checking
# if __name__ == "__main__":
#     import sys
#     sys.path.append("..")  # so it can find `utils`, `services`, etc.

#     sample_text = """
#     Pinecone is a vector database that lets you store, search, and retrieve high-dimensional vector representations of data.
#     It's commonly used with embeddings generated from models like OpenAI or SentenceTransformers in AI applications.
#     """
#     response = index_text_to_pinecone(sample_text, namespace="default")
#     print(response)

import os
import sys
from uuid import uuid4
from dotenv import load_dotenv
import google.generativeai as genai

# Ensure project root in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.chunk_text import get_text_chunks  # still useful for dividing long text

# --- Setup Gemini ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_text_with_gemini(text: str) -> str:
    """
    Use Gemini 2.0 Flash to summarize text.
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Summarize the following content in clear, structured points:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "No summary generated."
    except Exception as e:
        print(f"❌ Gemini summarization failed: {e}")
        return "Error during summarization."

def summarize_document(text: str) -> dict:
    """
    Splits a document into chunks, summarizes each chunk with Gemini,
    and returns all summaries combined.
    """
    chunks = get_text_chunks(text)
    summaries = []

    for i, chunk in enumerate(chunks):
        print(f"🧩 Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarize_text_with_gemini(chunk)
        summaries.append({
            "id": str(uuid4()),
            "chunk_index": i,
            "summary": summary
        })

    return {
        "message": f"Summarized {len(chunks)} chunks successfully.",
        "summaries": summaries
    }

# ---------- Local test ----------
if __name__ == "__main__":
    sample_text = """
    Pinecone is a vector database that lets you store, search, and retrieve high-dimensional vector representations of data.
    It's commonly used with embeddings generated from models like OpenAI or SentenceTransformers in AI applications.
    """

    response = summarize_document(sample_text)
    print(response)
