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

        for step in range(self.max_steps):
            screenshot = await device.screenshot()
            analysis = await self.vlm.analyze(
                screenshot=screenshot,
                command=command,
                model=current_model,
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
            result.actions.append({
                "step": step,
                "action": plan.next_action.to_dict(),
                "result": action_result,
            })

            if action_result.get("error"):
                retry_analysis = await self.vlm.analyze(
                    screenshot=await device.screenshot(),
                    command=f"Previous action failed: {action_result['error']}. {command}",
                    model=current_model,
                )
                plan = self.planner.plan(retry_analysis)

        return result
