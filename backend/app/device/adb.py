import asyncio
import subprocess
from dataclasses import dataclass


@dataclass
class ADBDevice:
    device_id: str
    model_name: str = "unknown"
    status: str = "offline"
    connection_type: str = "usb"

    async def _run(self, *args: str) -> str:
        cmd = ["adb", "-s", self.device_id, *args]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"ADB error: {stderr.decode().strip()}")
        return stdout.decode().strip()

    async def screenshot(self) -> bytes:
        proc = await asyncio.create_subprocess_exec(
            "adb", "-s", self.device_id, "exec-out", "screencap", "-p",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        return stdout

    async def tap(self, x: int, y: int):
        await self._run("shell", "input", "tap", str(x), str(y))

    async def swipe(self, x: int, y: int, direction: str = "up", distance: int = 500, duration: int = 300):
        dx, dy = {
            "up": (0, -distance),
            "down": (0, distance),
            "left": (-distance, 0),
            "right": (distance, 0),
        }.get(direction, (0, -distance))

        await self._run(
            "shell", "input", "swipe",
            str(x), str(y), str(x + dx), str(y + dy), str(duration),
        )

    async def type_text(self, text: str):
        escaped = text.replace(" ", "%s").replace("&", "\\&").replace("<", "\\<").replace(">", "\\>")
        await self._run("shell", "input", "text", escaped)

    async def press_back(self):
        await self._run("shell", "input", "keyevent", "KEYCODE_BACK")

    async def press_home(self):
        await self._run("shell", "input", "keyevent", "KEYCODE_HOME")

    async def press_recent(self):
        await self._run("shell", "input", "keyevent", "KEYCODE_APP_SWITCH")

    async def get_current_activity(self) -> str:
        output = await self._run("shell", "dumpsys", "activity", "activities")
        for line in output.splitlines():
            if "mResumedActivity" in line or "topResumedActivity" in line:
                return line.strip()
        return ""

    async def install_apk(self, path: str):
        await self._run("install", "-r", path)

    async def get_screen_resolution(self) -> tuple[int, int]:
        output = await self._run("shell", "wm", "size")
        size_str = output.split(":")[-1].strip()
        w, h = size_str.split("x")
        return int(w), int(h)

    @staticmethod
    def list_connected() -> list[str]:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True, text=True,
        )
        devices = []
        for line in result.stdout.strip().splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                devices.append(parts[0])
        return devices
