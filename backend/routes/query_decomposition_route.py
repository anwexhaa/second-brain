from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.query_decomposition_service import query_decomposition

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    namespace: str

@router.post("/query_decomposition")
async def run_query_decomposition(req: QueryRequest):
    try:
        answer = query_decomposition(req.question, req.namespace)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
