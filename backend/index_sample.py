from services.indexing_service import index_text_to_pinecone

sample_text = """
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+.
It is based on standard Python type hints. It was created by Sebastián Ramírez and is used by many big companies today.
"""

if __name__ == "__main__":
    result = index_text_to_pinecone(sample_text, namespace="demo")  # optional: change namespace name
    print(result)
