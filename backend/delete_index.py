from pinecone import Pinecone

print("🔥 Script started")

try:
    # Hardcoded credentials
    pc = Pinecone(
        api_key="pcsk_2envSW_ReK3Ys65VZh7DVsU468q5X97eqP3e5k6t9rvGCF2CtfVgzmN4kdXnBFqP4TkT1c"
    )
    print("✅ Pinecone client initialized")

    index_name = "second-brain-index"
    print("🔍 Checking index:", index_name)

    indexes = pc.list_indexes().names()
    print("📄 Existing indexes:", indexes)

    if index_name in indexes:
        pc.delete_index(index_name)
        print(f"🗑️ Deleted index: {index_name}")
    else:
        print(f"❌ Index '{index_name}' does not exist.")

except Exception as e:
    print("💥 Error occurred:", e)