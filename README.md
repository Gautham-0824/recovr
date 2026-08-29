# Recovr — Compliance-Bounded AI Revenue Recovery Agent

Recovr is an intelligent revenue recovery agent designed to recover lost subscriptions and recurring payments (UPI Autopay + card auto-debits) while strictly adhering to compliance policies (e.g., NPCI mandates, card association guidelines). 

Built for the **Razorpay AI Buildathon 2026** (Track 03: AI Revenue Recovery).

## Project Architecture
Recovr implements a robust, audited recovery pipeline across four distinct layers:

1. **Ingestion Layer**: Razorpay Webhook listener capture transaction failure events.
2. **Diagnosis Layer**: Classifies payment failures and evaluates recovery propensity.
3. **Policy Agent**: Constrained LLM selects recovery actions under compliance guardrails.
4. **Execution & Audit**: Triggers retries/messages and creates immutable audit logs.

## Compliance Rules
This system enforces strict compliance limits:
* **Max Attempts**: Up to 4 attempts per billing cycle (1 original payment + 3 retries).
* **Non-Peak Windows Only**: Retries scheduled only during designated non-peak hours (before 10:00 AM, 1:00 PM – 5:00 PM, and after 9:30 PM).
* **Time Spacing**: Inter-retry delays of 24h, 72h, and 7 days.
* **Hard/Soft Declines**:
  * Hard declines (`mandate_revoked`, `risk_decline`) skip retry schedules and trigger manual escalation.
  * Soft declines (`insufficient_funds`, `bank_timeout`) trigger scheduled retries.

## Directory Structure
```
recovr/
  backend/app/core/       # Compliance rules engine, diagnosis, agent, execution logic
  backend/app/models/     # Data models and schemas (ORM/Pydantic)
  backend/app/routers/    # Webhooks, batch processors, audit API routers
  backend/app/main.py     # FastAPI entry point
  backend/data/           # Synthetic generator scripts
  backend/requirements.txt
  backend/.env.example
  frontend/               # Next.js app (scaffolded later)
  docs/ARCHITECTURE.md
  README.md
  .gitignore
```

## Running the Verification Tests
To run compliance tests locally:
```bash
pytest backend/tests/
```
