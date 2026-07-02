from pydantic import BaseModel, Field
from typing import List


class Message(BaseModel):
    role: str = Field(..., examples=["user"])
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class Recommendation(BaseModel):
    name: str
    url: str
    reason: str


class ChatResponse(BaseModel):
    response: str
    recommendations: List[Recommendation] = []
    needs_clarification: bool = False