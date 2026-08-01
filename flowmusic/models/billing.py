from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class BillingEvent(BaseModel):
    event_at: datetime
    type: str
    amount: float
    max_created_at: datetime
    conversation_id: Optional[str] = None
    conversation_title: Optional[str] = None

class BillingSummary(BaseModel):
    events: List[BillingEvent]
