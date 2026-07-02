from fastapi import APIRouter
from app.models import ChatRequest, ChatResponse
from app.chatbot import chat

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok"
    }



@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    result = chat([m.model_dump() for m in request.messages])
    return ChatResponse(**result)