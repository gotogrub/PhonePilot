from dataclasses import dataclass

DEFAULT_SCREEN_W = 1080
DEFAULT_SCREEN_H = 2340


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
    ACTION_ALIASES = {
        "tap": "tap",
        "click": "tap",
        "press": "tap",
        "swipe": "swipe",
        "scroll": "swipe",
        "fling": "swipe",
        "type": "type",
        "input": "type",
        "enter_text": "type",
        "back": "back",
        "go_back": "back",
        "home": "home",
        "go_home": "home",
        "wait": "wait",
        "sleep": "wait",
    }

    VALID_DIRECTIONS = {"up", "down", "left", "right"}

    def plan(self, vlm_response: dict) -> Plan:
        action_type = vlm_response.get("action", "").strip().lower()
        reasoning = vlm_response.get("reasoning", "")

        if vlm_response.get("complete", False):
            return Plan(is_complete=True, reasoning=reasoning)

        action_type = self.ACTION_ALIASES.get(action_type, action_type)

        if not action_type:
            return Plan(is_complete=False, reasoning=reasoning)

        x = self._to_int(vlm_response.get("x"))
        y = self._to_int(vlm_response.get("y"))
        direction = vlm_response.get("direction", "")
        if isinstance(direction, str):
            direction = direction.strip().lower()
        text = vlm_response.get("text")

        if action_type == "tap":
            if x is None or y is None:
                return Plan(is_complete=False, reasoning=f"skip: tap without coordinates — {reasoning}")

        if action_type == "swipe":
            if x is None:
                x = DEFAULT_SCREEN_W // 2
            if y is None:
                y = DEFAULT_SCREEN_H // 2
            if direction not in self.VALID_DIRECTIONS:
                direction = "up"

        if action_type == "type" and not text:
            return Plan(is_complete=False, reasoning=f"skip: type without text — {reasoning}")

        action = Action(
            action_type=action_type,
            x=x,
            y=y,
            text=text,
            direction=direction if direction else None,
        )

        return Plan(next_action=action, reasoning=reasoning)

    @staticmethod
    def _to_int(val) -> int | None:
        if val is None:
            return None
        try:
            return int(val)
        except (TypeError, ValueError):
            return None
