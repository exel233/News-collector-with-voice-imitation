from fastapi import APIRouter

from app.api.routes_auth import router as auth_router
from app.api.routes_briefings import router as briefings_router
from app.api.routes_preferences import router as preferences_router
from app.api.routes_status import router as status_router
from app.api.routes_voice import router as voice_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(preferences_router)
api_router.include_router(briefings_router)
api_router.include_router(voice_router)
api_router.include_router(status_router)
