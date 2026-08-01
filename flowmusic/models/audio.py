from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime

class Duration(BaseModel):
    status: str
    value: Optional[str] = None

class LyricsData(BaseModel):
    id: str
    text: str

class Lyrics(BaseModel):
    status: str
    value: Optional[LyricsData] = None

class ClipOperation(BaseModel):
    op_type: str
    conversation_id: str
    sound_prompt: str
    title: str
    seed: Optional[str] = None
    lyrics_id: Optional[str] = None

class Clip(BaseModel):
    id: str
    author_id: str
    op_id: str
    op_type: str
    duration: Duration
    lyrics: Lyrics
    title: str
    privacy: str
    allow_public_use: bool
    created_at: datetime
    operation: ClipOperation
    audio_url: Optional[str] = None
    wav_url: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None

class ClipResponse(BaseModel):
    clips: Dict[str, Clip]
