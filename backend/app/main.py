from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import devices, models, scenarios, stream, tasks, voice
from app.config import settings
from app.memory.store import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
    app.include_router(devices.router, prefix="/devices", tags=["devices"])
    app.include_router(stream.router, prefix="/stream", tags=["stream"])
    app.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
    app.include_router(voice.router, prefix="/voice", tags=["voice"])
    app.include_router(models.router, prefix="/models", tags=["models"])

    return app


app = create_app()
