SYSTEM_PROMPT = """You are PhonePilot, an AI agent that controls an Android phone.
You see a screenshot of the phone screen and receive a user command.

Analyze the screenshot and determine the next action to take.

Respond in JSON format:
{
    "reasoning": "brief explanation of what you see and plan to do",
    "action": "tap|swipe|type|back|home|wait",
    "x": 500,
    "y": 800,
    "text": "text to type if action is type",
    "direction": "up|down|left|right if action is swipe",
    "complete": false
}

Set "complete": true when the user's task is accomplished.
Only output valid JSON, nothing else."""


def build_analysis_prompt(command: str) -> str:
    return f"{SYSTEM_PROMPT}\n\nUser command: {command}"


def build_retry_prompt(command: str, error: str) -> str:
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Previous action failed with error: {error}\n"
        f"User command: {command}\n"
        f"Please try a different approach."
    )


def build_context_prompt(command: str, history: list[dict]) -> str:
    history_text = "\n".join(
        f"- Step {h['step']}: {h['action']} -> {h['result']}"
        for h in history[-5:]
    )
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Previous actions:\n{history_text}\n\n"
        f"User command: {command}"
    )
