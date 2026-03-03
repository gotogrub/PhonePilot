from app.device.adb import ADBDevice


class DeviceActions:
    def __init__(self, device: ADBDevice):
        self.device = device

    async def open_app(self, package: str, activity: str | None = None):
        if activity:
            await self.device._run("shell", "am", "start", "-n", f"{package}/{activity}")
        else:
            await self.device._run(
                "shell", "monkey", "-p", package,
                "-c", "android.intent.category.LAUNCHER", "1",
            )

    async def close_app(self, package: str):
        await self.device._run("shell", "am", "force-stop", package)

    async def open_url(self, url: str):
        await self.device._run(
            "shell", "am", "start",
            "-a", "android.intent.action.VIEW",
            "-d", url,
        )

    async def set_clipboard(self, text: str):
        await self.device._run(
            "shell", "am", "broadcast",
            "-a", "clipper.set",
            "-e", "text", text,
        )

    async def get_installed_packages(self) -> list[str]:
        output = await self.device._run("shell", "pm", "list", "packages")
        return [line.replace("package:", "") for line in output.splitlines()]

    async def take_screenshot_to_file(self, local_path: str):
        data = await self.device.screenshot()
        with open(local_path, "wb") as f:
            f.write(data)
