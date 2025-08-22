from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.hyde_fusion_service import hyde_fusion

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    namespace: str = "default"

@router.post("/hyde_fusion_query")
async def run_hyde_fusion(req: QueryRequest):
    try:
        answer = hyde_fusion(req.question, req.namespace)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
