from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.hyde_service import hyde_query

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    namespace: str

@router.post("/hyde_query")
async def run_hyde_query(req: QueryRequest):
    try:
        answer = hyde_query(req.question, req.namespace)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
