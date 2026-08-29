"""
Policy Agent module.
Coordinates LLM-guided choices constrained by the rules engine.
"""

class PolicyAgent:
    def __init__(self):
        pass

    def decide(self, context, allowed_actions):
        """
        Choose the best action from the allowed action list.
        """
        # Under implementation
        return allowed_actions[0] if allowed_actions else None
