"""
Synthetic Data Generator.
Simulates subscription billing failures and webhook notifications.
"""
import random
from datetime import datetime, timedelta

def generate_failure_event():
    causes = ["insufficient_funds", "bank_timeout", "mandate_revoked", "risk_decline", "auth_failure"]
    cause = random.choice(causes)
    
    return {
        "event": "subscription.charged",
        "payment_id": f"pay_{random.randint(1000000000, 9999999999)}",
        "subscription_id": f"sub_{random.randint(100000000, 999999999)}",
        "error_code": f"ERR_{cause.upper()}",
        "error_description": f"Simulation failure for: {cause}",
        "cause": cause,
        "timestamp": datetime.utcnow().isoformat()
    }
