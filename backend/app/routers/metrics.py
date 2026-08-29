"""
Metrics Router.
Serves recovery success rate and dashboard stats.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/summary")
async def get_metrics():
    return {
        "recovery_rate": 0.0,
        "revenue_saved": 0.0,
        "active_mandates": 0,
        "total_failures": 0
    }
