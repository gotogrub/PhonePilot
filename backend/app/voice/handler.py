from app.voice.stt import WhisperSTT
from app.voice.tts import PiperTTS


class VoiceHandler:
    def __init__(self):
        self.stt = WhisperSTT()
        self.tts = PiperTTS()

    async def process_audio(self, audio_data: bytes) -> str:
        return await self.stt.transcribe(audio_data)

    async def speak(self, text: str) -> bytes:
        return await self.tts.synthesize(text)
