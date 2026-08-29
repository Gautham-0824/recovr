"""
Audit Router.
Serves historical log records of recovery decisions.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/logs")
async def get_audit_logs():
    return {"logs": []}
