# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from services.openai_services import get_embedding, get_answer
# from services.pinecone_services import query_pinecone
# from rag_a import answer_question

# router = APIRouter()

# class QueryRequest(BaseModel):
#     question: str
#     namespace: str

# @router.post("/")
# @router.post("")
# def ask_question(request: QueryRequest):
#     try:
#         question_embedding = get_embedding(request.question)
#         pinecone_results = query_pinecone(question_embedding)
        
#         print("pinecone matches:", pinecone_results['matches']) 

#         top_docs = [match['metadata']['text'] for match in pinecone_results['matches']]
#         context = "\n\n".join(top_docs)

#         print("combimed context:", context)

        
#         answer = answer_question(request.question, request.namespace)

#         return {"answer": answer}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag_a import answer_question

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    namespace: str

@router.post("/")
def ask_question(payload: QueryRequest):
    result = answer_question(payload.question, payload.namespace)
    return result


