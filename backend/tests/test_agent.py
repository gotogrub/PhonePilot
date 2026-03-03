from app.core.planner import Action, Planner
from app.vlm.parser import parse_vlm_response


def test_planner_tap():
    planner = Planner()
    plan = planner.plan({"action": "tap", "x": 100, "y": 200, "reasoning": "test"})
    assert plan.next_action.action_type == "tap"
    assert plan.next_action.x == 100
    assert plan.next_action.y == 200


def test_planner_complete():
    planner = Planner()
    plan = planner.plan({"complete": True, "reasoning": "done"})
    assert plan.is_complete


def test_parse_json_response():
    raw = '{"action": "tap", "x": 500, "y": 300, "reasoning": "found button", "complete": false}'
    result = parse_vlm_response(raw)
    assert result["action"] == "tap"
    assert result["x"] == 500


def test_parse_freeform_response():
    raw = "I see a button. I will tap 250, 400 to click it."
    result = parse_vlm_response(raw)
    assert result["action"] == "tap"
    assert result["x"] == 250
    assert result["y"] == 400


def test_action_to_dict():
    action = Action(action_type="tap", x=100, y=200)
    d = action.to_dict()
    assert d == {"action_type": "tap", "x": 100, "y": 200}
    assert "text" not in d
