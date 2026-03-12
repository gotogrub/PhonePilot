from abc import ABC, abstractmethod


class STTEngine(ABC):
    @abstractmethod
    async def transcribe(self, audio_data: bytes) -> str:
        ...


class WhisperSTT(STTEngine):
    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self._model = None

    async def transcribe(self, audio_data: bytes) -> str:
        raise NotImplementedError("Whisper integration pending")
