from abc import ABC, abstractmethod


class TTSEngine(ABC):
    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        ...


class PiperTTS(TTSEngine):
    def __init__(self, model_name: str = "en_US-lessac-medium"):
        self.model_name = model_name

    async def synthesize(self, text: str) -> bytes:
        raise NotImplementedError("Piper TTS integration pending")
