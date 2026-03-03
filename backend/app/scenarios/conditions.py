from dataclasses import dataclass


@dataclass
class Condition:
    condition_type: str
    target: str
    value: str | None = None
    operator: str = "contains"


class ConditionEvaluator:
    async def evaluate(self, condition: Condition, context: dict) -> bool:
        match condition.condition_type:
            case "screen_contains":
                return condition.target in context.get("screen_text", "")
            case "app_open":
                return condition.target in context.get("current_activity", "")
            case "time_after":
                from datetime import datetime
                target_time = datetime.fromisoformat(condition.target)
                return datetime.now() >= target_time
            case _:
                return False
