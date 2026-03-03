from dataclasses import dataclass


@dataclass
class Action:
    action_type: str
    x: int | None = None
    y: int | None = None
    text: str | None = None
    direction: str | None = None
    duration: int | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class Plan:
    next_action: Action | None = None
    is_complete: bool = False
    reasoning: str = ""


class Planner:
    ACTION_KEYWORDS = {
        "tap": "tap",
        "click": "tap",
        "swipe": "swipe",
        "scroll": "swipe",
        "type": "type",
        "input": "type",
        "back": "back",
        "home": "home",
    }

    def plan(self, vlm_response: dict) -> Plan:
        action_type = vlm_response.get("action", "")
        reasoning = vlm_response.get("reasoning", "")

        if vlm_response.get("complete", False):
            return Plan(is_complete=True, reasoning=reasoning)

        action = Action(
            action_type=action_type,
            x=vlm_response.get("x"),
            y=vlm_response.get("y"),
            text=vlm_response.get("text"),
            direction=vlm_response.get("direction"),
        )

        return Plan(next_action=action, reasoning=reasoning)
