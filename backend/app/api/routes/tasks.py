from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.agent import Agent
from app.device.manager import DeviceManager

router = APIRouter()


class TaskRequest(BaseModel):
    command: str
    device_id: str | None = None
    model: str | None = None


class TaskResponse(BaseModel):
    task_id: str
    status: str
    command: str
    actions: list[dict] = Field(default_factory=list)
    error: str | None = None


@router.post("", response_model=TaskResponse)
async def create_task(request: TaskRequest, db: AsyncSession = Depends(get_db)):
    task_id = str(uuid4())
    agent = Agent()
    device_manager = DeviceManager()

    device = await device_manager.get_device(request.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="No device found")

    try:
        result = await agent.execute(
            command=request.command,
            device=device,
            model=request.model,
            db=db,
        )
        return TaskResponse(
            task_id=task_id,
            status="completed",
            command=request.command,
            actions=result.actions,
        )
    except Exception as e:
        return TaskResponse(
            task_id=task_id,
            status="failed",
            command=request.command,
            error=str(e),
        )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    raise HTTPException(status_code=501, detail="Task history not yet implemented")
