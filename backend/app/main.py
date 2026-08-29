"""
Recovr Backend Application.
API endpoints for webhook ingestion, manual audits, and analytics.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import webhooks, batch, audit, metrics

app = FastAPI(
    title="Recovr Backend API",
    description="Bounded AI agent recovering failed UPI and card subscriptions for Razorpay Buildathon 2026",
    version="1.0.0"
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

@app.get("/")
async def root():
    return {
        "app": "Recovr API",
        "status": "healthy",
        "description": "UPI Autopay & Card Subscription AI Recovery Engine"
    }
