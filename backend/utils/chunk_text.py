import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', text)
    text = re.sub(r'(?<=[.,])(?=\S)', ' ', text)
    return text.strip()

def get_text_chunks(text: str) -> list[str]:
    try:
        cleaned_text = clean_text(text)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = splitter.split_text(cleaned_text)
        cleaned_chunks = [clean_text(chunk) for chunk in chunks]  # optional double clean
        return cleaned_chunks
    except Exception as e:
        print(f"Error while splitting text: {e}")
        return []

