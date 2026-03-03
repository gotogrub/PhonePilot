import asyncio
from collections.abc import Callable


class WakeWordDetector:
    def __init__(self, keyword: str = "hey pilot"):
        self.keyword = keyword
        self._running = False

    async def start(self, callback: Callable):
        self._running = True
        while self._running:
            await asyncio.sleep(0.1)

    def stop(self):
        self._running = False
