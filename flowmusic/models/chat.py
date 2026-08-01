from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class ChatPart(BaseModel):
    content: Optional[str] = None
    part_kind: str
    timestamp: Optional[str] = None
    tool_name: Optional[str] = None
    tool_call_id: Optional[str] = None
    args: Optional[Dict[str, Any]] = None

class ChatEvent(BaseModel):
    index: int
    status: str
    part: ChatPart
    delta: Optional[str] = ""

class ConversationResponse(BaseModel):
    job_id: str
