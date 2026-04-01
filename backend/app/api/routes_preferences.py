from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import User, UserSettings
from app.schemas.briefings import ScheduleResponse, UpdateScheduleRequest
from app.schemas.preferences import TopicResponse, UpdatePreferencesRequest, UpdateTopicsRequest, UserSettingsResponse
from app.services.news_pipeline import get_available_topics
from app.services.user_service import get_user_settings_bundle, update_user_preferences, update_user_topics


router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.get("", response_model=UserSettingsResponse)
def get_preferences(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_settings_bundle(db, user)


@router.put("", response_model=UserSettingsResponse)
def put_preferences(payload: UpdatePreferencesRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_user_preferences(db, user, payload)


@router.get("/topics", response_model=list[TopicResponse])
def list_topics(db: Session = Depends(get_db)):
    return get_available_topics(db)


@router.put("/topics", response_model=UserSettingsResponse)
def put_topics(payload: UpdateTopicsRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    update_user_topics(db, user, payload)
    return get_user_settings_bundle(db, user)


@router.get("/schedule", response_model=ScheduleResponse)
def get_schedule(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(UserSettings).filter(UserSettings.user_id == user.id).first()


@router.put("/schedule", response_model=ScheduleResponse)
def put_schedule(payload: UpdateScheduleRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    settings = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    settings.daily_schedule_time = payload.daily_schedule_time
    settings.briefing_length_minutes = payload.briefing_length_minutes
    settings.include_weekends = payload.include_weekends
    db.commit()
    db.refresh(settings)
    return settings
