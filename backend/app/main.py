from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.session import engine
from app.models import base  # noqa: F401
from app.db.session import SessionLocal
from app.services.auth_service import seed_topics
from app.tasks.scheduler import configure_scheduler, shutdown_scheduler


app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.on_event("startup")
def on_startup() -> None:
    base.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_topics(db)
    finally:
        db.close()
    configure_scheduler()


@app.on_event("shutdown")
def on_shutdown() -> None:
    shutdown_scheduler()
