# Pydantic models
from typing import List, Any, Dict, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"


class ChatResponse(BaseModel):
    reply: str
    agent_name: str
    tools_used: List[str] = []

class ChatHistory(BaseModel):
    user_id: str
    messages: List[Dict[str, Any]] = []

