import base64
import io

import httpx
from PIL import Image

from app.config import settings
from app.vlm.base import BaseVLM
from app.vlm.parser import parse_vlm_response
from app.vlm.prompts import SYSTEM_PROMPT, build_user_prompt

MAX_IMAGE_SIZE = 1280


def _resize_screenshot(raw_png: bytes) -> bytes:
    img = Image.open(io.BytesIO(raw_png))
    if max(img.size) > MAX_IMAGE_SIZE:
        ratio = MAX_IMAGE_SIZE / max(img.size)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class OllamaClient(BaseVLM):
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.active_model = settings.default_model

    async def analyze(
        self,
        screenshot: bytes,
        command: str,
        model: str | None = None,
        history: list[str] | None = None,
        screen_w: int = 1080,
        screen_h: int = 2340,
    ) -> dict:
        target_model = model or self.active_model
        resized = _resize_screenshot(screenshot)
        encoded_image = base64.b64encode(resized).decode("utf-8")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_prompt(command, history),
                "images": [encoded_image],
            },
        ]

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": target_model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 512,
                    },
                },
            )
            response.raise_for_status()
            data = response.json()

        raw_text = data.get("message", {}).get("content", "")
        parsed = parse_vlm_response(raw_text)

        if "x" in parsed and "y" in parsed:
            parsed["x"] = int(parsed["x"] * screen_w)
            parsed["y"] = int(parsed["y"] * screen_h)

        return parsed

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
