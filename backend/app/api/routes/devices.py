from fastapi import APIRouter
from pydantic import BaseModel

from app.device.manager import DeviceManager

router = APIRouter()


class DeviceInfo(BaseModel):
    device_id: str
    model: str
    status: str
    connection_type: str


class ConnectRequest(BaseModel):
    address: str
    port: int = 5555


@router.get("", response_model=list[DeviceInfo])
async def list_devices():
    manager = DeviceManager()
    devices = await manager.list_devices()
    return [
        DeviceInfo(
            device_id=d.device_id,
            model=d.model_name,
            status=d.status,
            connection_type=d.connection_type,
        )
        for d in devices
    ]


@router.post("/connect")
async def connect_device(request: ConnectRequest):
    manager = DeviceManager()
    device = await manager.connect_wifi(request.address, request.port)
    return {"status": "connected", "device_id": device.device_id}


@router.post("/{device_id}/disconnect")
async def disconnect_device(device_id: str):
    manager = DeviceManager()
    await manager.disconnect(device_id)
    return {"status": "disconnected"}
