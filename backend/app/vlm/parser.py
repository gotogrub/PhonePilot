import json
import re


def parse_vlm_response(raw: str) -> dict:
    tool_call = _extract_tool_call(raw)
    if tool_call:
        return _normalize_tool_call(tool_call, raw)

    json_match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    return _parse_freeform(raw)


def _parse_freeform(text: str) -> dict:
    result = {"reasoning": text, "action": "", "complete": False}
    text_lower = text.lower()

    patterns = {
        "tap": r"tap\s+(?:at\s+)?(\d+)\s*,?\s*(\d+)",
        "swipe": r"swipe\s+(up|down|left|right)",
        "type": r"type\s+[\"'](.+?)[\"']",
    }

    for action, pattern in patterns.items():
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

    if any(w in text_lower for w in ["complete", "done", "finished"]):
        result["complete"] = True

    return result


def _extract_tool_call(text: str) -> dict | None:
    match = re.search(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", text, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group(1))
        return data.get("arguments", data)
    except json.JSONDecodeError:
        return None


def _normalize_tool_call(args: dict, raw: str) -> dict:
    action = args.get("action", "")
    result = {
        "action": action,
        "reasoning": _extract_reasoning(raw),
        "complete": False,
    }

    if action == "click":
        result["action"] = "tap"
        coord = args.get("coordinate", [])
        if len(coord) >= 2:
            result["x"] = coord[0] / 999.0
            result["y"] = coord[1] / 999.0

    elif action == "swipe":
        coord = args.get("coordinate", [])
        coord2 = args.get("coordinate2", [])
        if len(coord) >= 2:
            result["x"] = coord[0] / 999.0
            result["y"] = coord[1] / 999.0
        if len(coord) >= 2 and len(coord2) >= 2:
            dx = coord2[0] - coord[0]
            dy = coord2[1] - coord[1]
            if abs(dx) > abs(dy):
                result["direction"] = "right" if dx > 0 else "left"
            else:
                result["direction"] = "down" if dy > 0 else "up"
        else:
            result["direction"] = "up"

    elif action == "type":
        result["text"] = args.get("text", "")

    elif action == "wait":
        result["duration"] = args.get("time", 1)

    elif action == "terminate":
        result["complete"] = True
        result["action"] = "wait"
        result["status"] = args.get("status", "success")

    return result


def _extract_reasoning(text: str) -> str:
    thought = re.search(r"Thought:\s*(.+?)(?:\n|$)", text)
    action_desc = re.search(r"Action:\s*(.+?)(?:\n|$)", text)
    parts = []
    if thought:
        parts.append(thought.group(1).strip())
    if action_desc:
        parts.append(action_desc.group(1).strip())
    return " | ".join(parts) if parts else text.split("<tool_call>")[0].strip()[:200]
