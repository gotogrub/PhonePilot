import json
import re


def parse_vlm_response(raw: str) -> dict:
    json_match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        pass

    return _parse_freeform(raw)


def _parse_freeform(text: str) -> dict:
    result = {"reasoning": text, "action": "", "complete": False}
    text_lower = text.lower()

    action_patterns = {
        "tap": r"tap\s+(?:at\s+)?(\d+)\s*,?\s*(\d+)",
        "swipe": r"swipe\s+(up|down|left|right)",
        "type": r"type\s+[\"'](.+?)[\"']",
    }

    for action, pattern in action_patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            result["action"] = action
            if action == "tap":
                result["x"] = int(match.group(1))
                result["y"] = int(match.group(2))
            elif action == "swipe":
                result["direction"] = match.group(1)
            elif action == "type":
                result["text"] = match.group(1)
            break

    if any(word in text_lower for word in ["complete", "done", "finished", "accomplished"]):
        result["complete"] = True

    return result
