# multi_route.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.multi_service import multi_query

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    namespace: str = "default"  # make it optional with default!

@router.post("/multi_query")
async def run_multi_query(req: QueryRequest):
    try:
        answer = multi_query(req.question, req.namespace)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
