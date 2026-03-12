from abc import ABC, abstractmethod


class BaseVLM(ABC):
    @abstractmethod
    async def analyze(self, screenshot: bytes, command: str, model: str | None = None) -> dict:
        ...

    @abstractmethod
    async def list_models(self) -> list[dict]:
        ...

    @abstractmethod
    async def set_active_model(self, model: str):
        ...
