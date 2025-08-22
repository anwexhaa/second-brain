from services.openai_services import generate_hypothetical_answer, get_embedding
from services.pinecone_services import query_pinecone

def hyde_query(question: str, namespace: str = "default") -> str:
    # Step 1: Generate hypothetical answer from the user's question
    hypothetical_answer = generate_hypothetical_answer(question)

    # Step 2: Embed the hypothetical answer
    embedding = get_embedding(hypothetical_answer)
    if not embedding:
        return "❌ Error generating embedding."

    # Step 3: Query Pinecone with the embedding
    results = query_pinecone(query_embedding=embedding, namespace=namespace)
    if not results:
        return "❌ No results from Pinecone."

    # Step 4: Extract context chunks from matched metadata
    contexts = [
        match["metadata"].get("text", "")
        for match in results
        if match and "metadata" in match
    ]

    if not any(contexts):
        return "❌ No usable context found in Pinecone results."

    # Step 5: Construct final prompt
    context_str = "\n\n".join(contexts)
    final_prompt = f"Answer the question based on the context below:\n\nContext:\n{context_str}\n\nQuestion: {question}"

    # Step 6: Return the final answer
    return generate_hypothetical_answer(final_prompt)
