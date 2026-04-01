from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import User
from app.schemas.voice import VoiceProfileResponse
from app.services.briefing_service import get_or_create_voice_profile
from app.services.voice_service import store_voice_sample


router = APIRouter(prefix="/voice", tags=["voice"])


@router.get("", response_model=VoiceProfileResponse)
def get_voice_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_or_create_voice_profile(db, user)


@router.post("/sample", response_model=VoiceProfileResponse)
async def upload_voice_sample(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return store_voice_sample(db, user, file.filename, await file.read())
