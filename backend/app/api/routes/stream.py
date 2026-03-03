import asyncio
import base64

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.device.manager import DeviceManager

router = APIRouter()


@router.websocket("/{device_id}")
async def device_stream(websocket: WebSocket, device_id: str):
    await websocket.accept()
    manager = DeviceManager()

    try:
        device = await manager.get_device(device_id)
        if not device:
            await websocket.close(code=4004, reason="Device not found")
            return

        while True:
            screenshot = await device.screenshot()
            encoded = base64.b64encode(screenshot).decode("utf-8")
            await websocket.send_json({
                "type": "frame",
                "data": encoded,
                "device_id": device_id,
            })
            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        pass
    except Exception:
        await websocket.close(code=4000)
