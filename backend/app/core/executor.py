import asyncio

from app.config import settings
from app.core.planner import Action


class ActionExecutor:
    async def execute(self, device, action: Action) -> dict:
        try:
            match action.action_type:
                case "tap":
                    await device.tap(action.x, action.y)
                case "swipe":
                    await device.swipe(
                        action.x, action.y,
                        direction=action.direction or "up",
                    )
                case "type":
                    await device.type_text(action.text or "")
                case "back":
                    await device.press_back()
                case "home":
                    await device.press_home()
                case "wait":
                    await asyncio.sleep(action.duration or settings.action_delay)
                case _:
                    return {"error": f"Unknown action: {action.action_type}"}

            await asyncio.sleep(settings.action_delay)
            return {"status": "success", "action": action.action_type}

        except Exception as e:
            return {"error": str(e), "action": action.action_type}
