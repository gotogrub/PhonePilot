import asyncio
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScheduledTask:
    scenario_name: str
    cron_expression: str
    device_id: str
    enabled: bool = True
    last_run: datetime | None = None
    next_run: datetime | None = None


class Scheduler:
    def __init__(self):
        self._tasks: dict[str, ScheduledTask] = {}
        self._running = False

    def add(self, task: ScheduledTask):
        self._tasks[task.scenario_name] = task

    def remove(self, scenario_name: str):
        self._tasks.pop(scenario_name, None)

    def list_tasks(self) -> list[ScheduledTask]:
        return list(self._tasks.values())

    async def start(self):
        self._running = True
        while self._running:
            await asyncio.sleep(60)

    def stop(self):
        self._running = False
