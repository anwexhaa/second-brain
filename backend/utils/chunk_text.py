import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def clean_text(text: str) -> str:
    """
    Cleans the text by normalizing spaces and adding spaces between words and numbers/punctuation.
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', text)
    text = re.sub(r'(?<=[.,!?])(?=\S)', ' ', text)
    return text.strip()

def get_text_chunks(text: str) -> list[str]:
    """
    Splits the text into reasonably sized chunks with overlap to preserve context.
    Optimized for PDF content in RAG pipelines.
    """
    try:
        cleaned_text = clean_text(text)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,        # larger chunk size for context
            chunk_overlap=400,      # overlap to retain context across chunks
            separators=["\n\n", "\n", ".", " "]
        )
        chunks = splitter.split_text(cleaned_text)
        # optional second cleaning to remove stray whitespace/newlines
        cleaned_chunks = [clean_text(chunk) for chunk in chunks if chunk.strip()]
        return cleaned_chunks
    except Exception as e:
        print(f"Error while splitting text: {e}")
        return []
