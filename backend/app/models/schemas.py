"""
Schemas module.
Pydantic schemas for request validation.
"""
from pydantic import BaseModel
from datetime import datetime

class WebhookPayload(BaseModel):
    event: str
    payment_id: str
    subscription_id: str
    error_code: str
    error_description: str
    timestamp: datetime
