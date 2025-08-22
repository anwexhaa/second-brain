from services.pinecone_services import index

namespace = "test"
print(f"\n📦 Fetching vectors in namespace: {namespace}")

stats = index.describe_index_stats()
vector_count = stats.namespaces.get(namespace, {}).get("vector_count", 0)
print("Total vectors:", vector_count)

# Query dummy vector just to retrieve some metadata
res = index.query(
    vector=[0.0] * 384,
    top_k=2,
    include_metadata=True,
    namespace=namespace
)

for match in res.matches:
    print("\n💬 Text:", match.metadata.get("text", ""))
    print("📄 Source:", match.metadata.get("source", "unknown"))
