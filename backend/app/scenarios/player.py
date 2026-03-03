import asyncio

from app.core.executor import ActionExecutor
from app.core.planner import Action


class ScenarioPlayer:
    def __init__(self):
        self.executor = ActionExecutor()
        self._is_playing = False

    async def play(self, scenario: dict, device) -> list[dict]:
        self._is_playing = True
        results = []

        for step in scenario.get("steps", []):
            if not self._is_playing:
                break

            action = Action(
                action_type=step.get("action", ""),
                x=step.get("x"),
                y=step.get("y"),
                text=step.get("value"),
                direction=step.get("direction"),
            )

            if step.get("wait"):
                await asyncio.sleep(float(step["wait"]))

            result = await self.executor.execute(device, action)
            results.append(result)

        self._is_playing = False
        return results

    def stop(self):
        self._is_playing = False
