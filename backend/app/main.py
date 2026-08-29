"""
Recovr Backend Application.
API endpoints for webhook ingestion, manual audits, and analytics.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import webhooks, batch, audit, metrics

# Wire in the rules engine — exposes compliance constants at startup
from app.core.rules_engine import (
    MAX_ATTEMPTS_PER_CYCLE,
    RETRY_SPACING_HOURS,
    NON_PEAK_WINDOWS,
    HARD_DECLINE_CAUSES,
)

app = FastAPI(
    title="Recovr Backend API",
    description=(
        "Bounded AI agent recovering failed UPI and card subscriptions "
        "for Razorpay Buildathon 2026"
    ),
    version="1.0.0",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(webhooks.router)
app.include_router(batch.router)
app.include_router(audit.router)
app.include_router(metrics.router)


@app.get("/health", tags=["Health"])
async def health():
    """Liveness probe — used by Render and load balancers."""
    return {"status": "ok"}


@app.get("/", tags=["Root"])
async def root():
    """Root info endpoint — also exposes wired compliance constants."""
    return {
        "app": "Recovr API",
        "version": "1.0.0",
        "description": "UPI Autopay & Card Subscription AI Recovery Engine",
        "compliance": {
            "max_attempts_per_cycle": MAX_ATTEMPTS_PER_CYCLE,
            "retry_spacing_hours": RETRY_SPACING_HOURS,
            "hard_decline_causes": [c.value for c in HARD_DECLINE_CAUSES],
        },
    }
