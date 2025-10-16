from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth.database import init_db


from .config import get_settings
from .routers import admin, analysis, auth, chat, data, health, pose, tasks
from .state import init_state


def create_app() -> FastAPI:
    settings = get_settings()
    init_state(settings)
    init_db()

    app = FastAPI(title="RunData API", version="1.0.0")

    origins = settings.cors_allow_origins or ["*"]
    allow_credentials = "*" not in origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(data.router)
    app.include_router(analysis.router)
    app.include_router(chat.router)
    app.include_router(admin.router)
    app.include_router(pose.router)
    app.include_router(tasks.router)

    app.mount("/tmp", StaticFiles(directory=settings.pose_tmp_dir), name="tmp")
    uploads_dir = Path(__file__).resolve().parent.parent / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

    return app
app = create_app()
