import unittest
import os
import difflib
from datetime import datetime

# Adjust Python path to allow app import when run directly
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.rules_engine import FailureCause, Action, RecoveryContext, allowed_actions, evaluate

EXPECTED_CODE = """from dataclasses import dataclass
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
    }"""

class TestComplianceEngine(unittest.TestCase):
    def test_insufficient_funds_attempt_1(self):
        # Assertion 1: insufficient_funds attempt 1 -> allowed_actions contains retry_scheduled
        ctx = RecoveryContext(
            cause=FailureCause.INSUFFICIENT_FUNDS,
            attempt_number=1,
            last_attempt_at=None,
            now=datetime.utcnow()
        )
        actions = allowed_actions(ctx)
        self.assertIn(Action.RETRY_SCHEDULED, actions)

    def test_mandate_revoked_any_attempt_1_to_3(self):
        # Assertion 2: mandate_revoked at ANY attempt number 1-3 -> never contains retry_scheduled or retry_now
        for attempt in range(1, 4):
            ctx = RecoveryContext(
                cause=FailureCause.MANDATE_REVOKED,
                attempt_number=attempt,
                last_attempt_at=None,
                now=datetime.utcnow()
            )
            actions = allowed_actions(ctx)
            self.assertNotIn(Action.RETRY_SCHEDULED, actions)
            self.assertNotIn(Action.RETRY_NOW, actions)

    def test_attempt_number_4_any_cause(self):
        # Assertion 3: attempt_number=4 for any cause -> allowed_actions == [stop_write_off] exactly
        for cause in FailureCause:
            ctx = RecoveryContext(
                cause=cause,
                attempt_number=4,
                last_attempt_at=None,
                now=datetime.utcnow()
            )
            actions = allowed_actions(ctx)
            self.assertEqual(actions, [Action.STOP_WRITE_OFF])

    def test_verbatim_file_content(self):
        # Assertion 4: diff the file you wrote against the expected code block and confirm it's identical
        rules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'core', 'rules_engine.py'))
        with open(rules_path, 'r', encoding='utf-8') as f:
            actual_content = f.read()

        # Normalize line endings to avoid OS discrepancies in verification
        actual_normalized = actual_content.replace('\r\n', '\n').strip()
        expected_normalized = EXPECTED_CODE.replace('\r\n', '\n').strip()

        if actual_normalized != expected_normalized:
            diff = difflib.unified_diff(
                expected_normalized.splitlines(keepends=True),
                actual_normalized.splitlines(keepends=True),
                fromfile='expected_code',
                tofile='rules_engine.py'
            )
            diff_str = "".join(diff)
            self.fail(f"rules_engine.py is not identical to verbatim block:\n{diff_str}")

if __name__ == '__main__':
    unittest.main()
