from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "PhonePilot"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    database_url: str = "sqlite+aiosqlite:///./phonepilot.db"

    redis_url: str = "redis://localhost:6379/0"

    ollama_base_url: str = "http://localhost:11434"
    default_model: str = "qwen2.5vl:7b"

    adb_host: str = "127.0.0.1"
    adb_port: int = 5037

    screenshot_dir: str = "./screenshots"
    max_steps: int = 10
    max_retries: int = 3
    action_delay: float = 1.0

    whisper_model: str = "base"
    tts_model: str = "en_US-lessac-medium"
    wake_word: str = "hey pilot"

    model_config = {"env_prefix": "PHONEPILOT_", "env_file": ".env"}


settings = Settings()
