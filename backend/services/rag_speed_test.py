import time
from services.rag_fusion_services import rag_fusion

if __name__ == "__main__":
    test_question = "How do knowledge graphs help in RAG?"
    test_namespace = "default"

    start_time = time.time()
    answer = rag_fusion(test_question, namespace=test_namespace)
    end_time = time.time()

    print("\n📌 Question:", test_question)
    print("\n💬 Answer:\n", answer)
    print(f"\n⏱️ Total time taken: {end_time - start_time:.2f} seconds")
