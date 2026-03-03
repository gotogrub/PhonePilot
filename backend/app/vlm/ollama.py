import base64

import httpx

from app.config import settings
from app.vlm.base import BaseVLM
from app.vlm.parser import parse_vlm_response
from app.vlm.prompts import build_analysis_prompt


class OllamaClient(BaseVLM):
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.active_model = settings.default_model

    async def analyze(self, screenshot: bytes, command: str, model: str | None = None) -> dict:
        target_model = model or self.active_model
        encoded_image = base64.b64encode(screenshot).decode("utf-8")
        prompt = build_analysis_prompt(command)

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": target_model,
                    "prompt": prompt,
                    "images": [encoded_image],
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 512,
                    },
                },
            )
            response.raise_for_status()
            data = response.json()

        return parse_vlm_response(data.get("response", ""))

    async def list_models(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()

        return [
            {
                "name": m["name"],
                "size": f"{m.get('size', 0) / 1e9:.1f}GB",
                "active": m["name"] == self.active_model,
            }
            for m in data.get("models", [])
        ]

    async def set_active_model(self, model: str):
        self.active_model = model
