import asyncio

from app.device.adb import ADBDevice


class DeviceManager:
    _devices: dict[str, ADBDevice] = {}

    async def list_devices(self) -> list[ADBDevice]:
        connected = await asyncio.to_thread(ADBDevice.list_connected)
        for device_id in connected:
            if device_id not in self._devices:
                device = ADBDevice(
                    device_id=device_id,
                    status="online",
                    connection_type="wifi" if ":" in device_id else "usb",
                )
                self._devices[device_id] = device
            else:
                self._devices[device_id].status = "online"

        offline = set(self._devices.keys()) - set(connected)
        for device_id in offline:
            self._devices[device_id].status = "offline"

        return list(self._devices.values())

    async def get_device(self, device_id: str | None = None) -> ADBDevice | None:
        await self.list_devices()

        if device_id:
            return self._devices.get(device_id)

        for device in self._devices.values():
            if device.status == "online":
                return device
        return None

    async def connect_wifi(self, address: str, port: int = 5555) -> ADBDevice:
        target = f"{address}:{port}"
        proc = await asyncio.create_subprocess_exec(
            "adb", "connect", target,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        output = stdout.decode().strip()

        if "connected" not in output.lower():
            raise RuntimeError(f"Failed to connect: {output}")

        device = ADBDevice(
            device_id=target,
            status="online",
            connection_type="wifi",
        )
        self._devices[target] = device
        return device

    async def disconnect(self, device_id: str):
        if device_id in self._devices:
            if ":" in device_id:
                proc = await asyncio.create_subprocess_exec(
                    "adb", "disconnect", device_id,
                    stdout=asyncio.subprocess.PIPE,
                )
                await proc.communicate()
            del self._devices[device_id]
