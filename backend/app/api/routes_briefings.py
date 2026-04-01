from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.models import User
from app.schemas.briefings import BriefingListResponse, BriefingResponse, GenerateBriefingRequest
from app.schemas.voice import AudioResponse
from app.services.briefing_service import generate_briefing_for_user, get_briefing_for_user, list_briefings_for_user


router = APIRouter(prefix="/briefings", tags=["briefings"])


@router.post("/generate", response_model=BriefingResponse)
def generate_briefing(payload: GenerateBriefingRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return generate_briefing_for_user(db, user, mode=payload.mode)


@router.get("", response_model=BriefingListResponse)
def list_briefings(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"items": list_briefings_for_user(db, user)}


@router.get("/{briefing_id}", response_model=BriefingResponse)
def get_briefing(briefing_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    briefing = get_briefing_for_user(db, user, briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing not found")
    return briefing


@router.get("/{briefing_id}/audio", response_model=AudioResponse)
def get_audio(briefing_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    briefing = get_briefing_for_user(db, user, briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing not found")
    return {
        "briefing_id": briefing_id,
        "audio_url": f"{settings.backend_public_url}{briefing.audio_path}" if briefing.audio_path else None,
        "fallback_mode": "standard_tts" if briefing.audio_path else "browser_speech_synthesis",
        "script": briefing.script,
    }


@router.get("/media/{filename}")
def get_media(filename: str):
    path = Path(settings.media_dir) / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(path)
