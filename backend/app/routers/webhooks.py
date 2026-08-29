"""
Webhooks Router.
Ingests failed payment events from Razorpay.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/razorpay")
async def handle_razorpay_webhook():
    return {"message": "Webhook received"}
