from fastapi import APIRouter
from pydantic import BaseModel

from app.vlm.ollama import OllamaClient

router = APIRouter()


class ModelInfo(BaseModel):
    name: str
    size: str
    active: bool


class SwitchRequest(BaseModel):
    model: str


@router.get("", response_model=list[ModelInfo])
async def list_models():
    client = OllamaClient()
    models = await client.list_models()
    return models


@router.post("/switch")
async def switch_model(request: SwitchRequest):
    client = OllamaClient()
    await client.set_active_model(request.model)
    return {"status": "switched", "model": request.model}
