from services.pinecone_services import index
from rag_a import answer_question

# --- Show available namespaces ---
stats = index.describe_index_stats()
print("Available namespaces:", stats.namespaces)
print("Test namespace stats:", stats.namespaces.get("test", {}))

# --- Test a sample question ---
question = "Summarize the uploaded content"
namespace = "test"  # Or "default", "notes", etc., based on your uploads

print("\n🔎 Asking:", question)
response = answer_question(question, namespace)

print("\n✅ Answer:\n", response["answer"])
print("\n📄 Matches:")
for match in response["matches"]:
    print(f"- Score: {match['score']:.2f} | Source: {match['source']}")
    print(f"  Text: {match['text'][:200]}...\n")
