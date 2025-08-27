from fastapi import FastAPI
from routes import upload
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from services.openai_services import get_embedding
from routes import ask, test_embed, index
from routes.test_embed import router as test_embed_router
from rag_a import answer_question
from pydantic import BaseModel
from routes import hyde_router
from routes import multi_route
from routes import rag_fusion_route
from routes import query_decomposition_route
from routes import hyde_fusion_route
import os  # <--- Add this

# from utils.auth_middleware import firebase_auth_middleware  # Updated middleware

load_dotenv()
app = FastAPI()

# ------------------ ROOT ROUTE ------------------
@app.get("/")
def read_root():
    return {"message": "Backend is running!"}


# ------------------ MIDDLEWARE ------------------
frontend_url = os.getenv("FRONTEND_URL", "https://second-brain-fawn.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase + Supabase auth middleware applied globally
# app.middleware("http")(firebase_auth_middleware)

# ------------------ ROUTES ------------------
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(ask.router, prefix="/ask", tags=["ask"])
app.include_router(test_embed.router, prefix="/test", tags=["test"])
app.include_router(index.router, prefix="/index", tags=["index"])
app.include_router(hyde_router.router, prefix="/hyde", tags=["hyde"])
app.include_router(multi_route.router, prefix="/multi", tags=["multi"])
app.include_router(rag_fusion_route.router, prefix="/rag_fusion", tags=["rag_fusion"])
app.include_router(query_decomposition_route.router, prefix="/query_decomposition", tags=["query_decomposition"])
app.include_router(hyde_fusion_route.router, prefix="/hyde_fusion", tags=["hyde_fusion"])

# ------------------ STARTUP EVENT ------------------
@app.on_event("startup")
async def startup_event():    
    text = "Artificial intelligence is reshaping industries and driving innovation."
    embedding = get_embedding(text)
    print("Sample embedding (first 5):", embedding[:5])
    print("Embedding length:", len(embedding))

# ------------------ DEBUG QUERY ------------------
class DebugQueryRequest(BaseModel):
    question: str
    namespace: str 

@app.post("/debug-query")
def debug_query(payload: DebugQueryRequest):
    from services.pinecone_services import query_pinecone
    from services.openai_services import get_embedding

    embedding = get_embedding(payload.question)
    results = query_pinecone(embedding, namespace=payload.namespace)

    # Safely return only the match summaries
    safe_output = []
    for match in results.get("matches", []):
        safe_output.append({
            "id": match.get("id"),
            "score": match.get("score"),
            "text": match.get("metadata", {}).get("text")
        })

    return {"matches": safe_output}
