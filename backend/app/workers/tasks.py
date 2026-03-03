import asyncio

from app.core.agent import Agent
from app.device.manager import DeviceManager


def execute_task(command: str, device_id: str | None = None, model: str | None = None) -> dict:
    return asyncio.run(_execute_task(command, device_id, model))


async def _execute_task(command: str, device_id: str | None, model: str | None) -> dict:
    agent = Agent()
    manager = DeviceManager()
    device = await manager.get_device(device_id)

    if not device:
        return {"status": "error", "error": "No device available"}

    result = await agent.execute(command=command, device=device, model=model)
    return {
        "status": "completed" if result.success else "failed",
        "actions": result.actions,
        "error": result.error,
    }
