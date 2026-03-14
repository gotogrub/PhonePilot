from dataclasses import dataclass, field

from app.config import settings
from app.core.executor import ActionExecutor
from app.core.planner import Planner
from app.vlm.ollama import OllamaClient


@dataclass
class AgentResult:
    actions: list[dict] = field(default_factory=list)
    success: bool = False
    error: str | None = None


class Agent:
    def __init__(self):
        self.vlm = OllamaClient()
        self.planner = Planner()
        self.executor = ActionExecutor()
        self.max_steps = settings.max_steps

    async def execute(self, command: str, device, model: str | None = None, db=None) -> AgentResult:
        result = AgentResult()
        current_model = model or settings.default_model
        action_history: list[str] = []

        try:
            screen_w, screen_h = await device.get_screen_resolution()
        except Exception:
            screen_w, screen_h = 1080, 2340

        for step in range(self.max_steps):
            screenshot = await device.screenshot()
            analysis = await self.vlm.analyze(
                screenshot=screenshot,
                command=command,
                model=current_model,
                history=action_history if action_history else None,
                screen_w=screen_w,
                screen_h=screen_h,
            )

            plan = self.planner.plan(analysis)
            if plan.is_complete:
                result.success = True
                break

            if plan.next_action is None:
                result.actions.append({
                    "step": step,
                    "action": {"skipped": plan.reasoning},
                    "result": {"status": "skipped"},
                })
                continue

            action_result = await self.executor.execute(device, plan.next_action)
            action_desc = plan.next_action.action_type
            if plan.next_action.text:
                action_desc += f" '{plan.next_action.text}'"
            action_history.append(action_desc)

            result.actions.append({
                "step": step,
                "action": plan.next_action.to_dict(),
                "reasoning": plan.reasoning,
                "result": action_result,
            })

            if action_result.get("error"):
                retry_analysis = await self.vlm.analyze(
                    screenshot=await device.screenshot(),
                    command=f"Previous action failed: {action_result['error']}. {command}",
                    model=current_model,
                    history=action_history,
                    screen_w=screen_w,
                    screen_h=screen_h,
                )
                plan = self.planner.plan(retry_analysis)

        return result
