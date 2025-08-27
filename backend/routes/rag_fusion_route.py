from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag_fusion_services import rag_fusion
from services.openai_services import generate_hypothetical_answer  # Gemini

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    namespace: str = "default"

GREETINGS = ["hi", "hello", "hey", "yo", "sup", "greetings","howdy", "what's up", "hi there", "hey there"]

def is_greeting(message: str) -> bool:
    return message.strip().lower() in GREETINGS

def is_conversational(message: str) -> bool:
    message = message.lower()
    return any(phrase in message for phrase in [
        "can you", "help me", "i don’t know", "idk", "wtf", "what do i do",
        "what now", "okay so", "bro", "babe", "dude", "how do i start", 
        "how are you", "what's up", "what's going on", "what's happening",
        "what's the deal", "what's the story"
    ])

@router.post("/rag_fusion_query")
async def run_rag_fusion(req: QueryRequest):
    try:
        user_input = req.question.strip()

        # 🎯 Greeting
        if is_greeting(user_input):
            return {"answer": "Hey there! What can I help you with today? 😊"}

        # 💬 Casual conversation fallback
        if is_conversational(user_input):
            prompt = f"""
You're a friendly AI assistant. Respond naturally like you're talking to a friend.
Keep it short and playful.

User: {user_input}
Assistant:"""
            response = generate_hypothetical_answer(prompt)
            return {"answer": response or "Hmm, not sure how to respond — mind rephrasing?"}

        # 🔍 Only query RAG if the question is likely factual / about uploaded docs
        factual_keywords = ["overview", "features", "architecture", "technical", "details", "specs", "implementation"]
        if any(k in user_input.lower() for k in factual_keywords):
            answer_data = rag_fusion(user_input, req.namespace)
            return {"answer": answer_data.get("answer", "❌ Sorry, couldn't find anything."), 
                    "matches": answer_data.get("matches", [])}

        # 🗣 For anything else, fallback to conversational Gemini
        prompt = f"""
You're a helpful AI assistant. Respond naturally to the user's question.

User: {user_input}
Assistant:"""
        response = generate_hypothetical_answer(prompt)
        return {"answer": response or "Hmm, not sure how to respond — mind rephrasing?"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
