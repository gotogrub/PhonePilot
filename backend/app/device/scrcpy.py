import asyncio
from dataclasses import dataclass


@dataclass
class ScrcpySession:
    device_id: str
    process: asyncio.subprocess.Process | None = None
    port: int = 8099

    async def start(self, max_size: int = 1024, bitrate: int = 2_000_000):
        self.process = await asyncio.create_subprocess_exec(
            "scrcpy",
            "--serial", self.device_id,
            "--max-size", str(max_size),
            "--video-bit-rate", str(bitrate),
            "--no-audio",
            "--no-control",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    async def stop(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()
            self.process = None

    @property
    def is_running(self) -> bool:
        return self.process is not None and self.process.returncode is None
