from dataclasses import dataclass
from datetime import datetime, time, timedelta
from enum import Enum

class FailureCause(str, Enum):
    INSUFFICIENT_FUNDS = "insufficient_funds"
    BANK_TIMEOUT = "bank_timeout"
    MANDATE_REVOKED = "mandate_revoked"
    RISK_DECLINE = "risk_decline"
    AUTH_FAILURE = "auth_failure"

class Action(str, Enum):
    RETRY_NOW = "retry_now"
    RETRY_SCHEDULED = "retry_scheduled"
    CHANNEL_SWITCH_NUDGE = "channel_switch_nudge"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    STOP_WRITE_OFF = "stop_write_off"

MAX_ATTEMPTS_PER_CYCLE = 4
RETRY_SPACING_HOURS = [24, 72, 168]
NON_PEAK_WINDOWS = [(time(0,0), time(10,0)), (time(13,0), time(17,0)), (time(21,30), time(23,59))]
HARD_DECLINE_CAUSES = {FailureCause.MANDATE_REVOKED, FailureCause.RISK_DECLINE}

@dataclass
class RecoveryContext:
    cause: FailureCause
    attempt_number: int
    last_attempt_at: datetime | None
    now: datetime

def is_non_peak(ts: datetime) -> bool:
    t = ts.time()
    return any(start <= t <= end for start, end in NON_PEAK_WINDOWS)

def next_eligible_retry_time(ctx: RecoveryContext) -> datetime | None:
    if ctx.attempt_number > len(RETRY_SPACING_HOURS):
        return None
    spacing = RETRY_SPACING_HOURS[ctx.attempt_number - 1]
    base = ctx.last_attempt_at or ctx.now
    candidate = base + timedelta(hours=spacing)
    guard = 0
    while not is_non_peak(candidate) and guard < 48:
        candidate += timedelta(minutes=30)
        guard += 1
    return candidate

def allowed_actions(ctx: RecoveryContext) -> list[Action]:
    if ctx.attempt_number >= MAX_ATTEMPTS_PER_CYCLE:
        return [Action.STOP_WRITE_OFF]
    if ctx.cause in HARD_DECLINE_CAUSES:
        return [Action.CHANNEL_SWITCH_NUDGE, Action.ESCALATE_TO_HUMAN]
    if ctx.cause == FailureCause.AUTH_FAILURE:
        return [Action.CHANNEL_SWITCH_NUDGE, Action.RETRY_SCHEDULED]
    return [Action.RETRY_SCHEDULED, Action.CHANNEL_SWITCH_NUDGE]

def evaluate(ctx: RecoveryContext) -> dict:
    return {
        "allowed_actions": [a.value for a in allowed_actions(ctx)],
        "next_eligible_retry_time": next_eligible_retry_time(ctx),
        "attempts_remaining": max(0, MAX_ATTEMPTS_PER_CYCLE - ctx.attempt_number),
        "rule_applied": (
            "hard_decline_no_retry" if ctx.cause in HARD_DECLINE_CAUSES
            else "max_attempts_reached" if ctx.attempt_number >= MAX_ATTEMPTS_PER_CYCLE
            else "soft_decline_scheduled_retry"
        ),
    }
