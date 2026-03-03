from abc import ABC, abstractmethod


class BaseVLM(ABC):
    @abstractmethod
    async def analyze(
        self,
        screenshot: bytes,
        command: str,
        model: str | None = None,
        history: list[str] | None = None,
        screen_w: int = 1080,
        screen_h: int = 2340,
    ) -> dict:
        ...

    @abstractmethod
    async def list_models(self) -> list[dict]:
        ...

    @abstractmethod
    async def set_active_model(self, model: str):
        ...
