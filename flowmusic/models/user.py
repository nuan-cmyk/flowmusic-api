from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    username: str
    is_member: bool

class UserLevel(BaseModel):
    upgraded: bool
    level: str

class UserScores(BaseModel):
    level: str
    score: float
    create_longest_streak: int
