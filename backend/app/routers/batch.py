"""
Batch Router.
Triggers batch recovery execution and cron checkups.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/batch", tags=["Batch"])

@router.post("/process-retries")
async def process_retries():
    return {"message": "Batch retries processed"}
