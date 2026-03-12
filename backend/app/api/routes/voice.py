from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

router = APIRouter()


class VoiceCommandResponse(BaseModel):
    text: str
    task_id: str | None = None
    status: str


@router.post("/command", response_model=VoiceCommandResponse)
async def voice_command(audio: UploadFile = File(...)):
    audio_data = await audio.read()
    _ = audio_data
    return VoiceCommandResponse(
        text="",
        status="not_implemented",
    )


@router.get("/status")
async def voice_status():
    return {
        "stt_available": False,
        "tts_available": False,
        "wake_word_active": False,
    }
