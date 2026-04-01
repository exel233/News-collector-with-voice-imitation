from sqlalchemy.orm import Session, joinedload

from app.models.models import Topic, User, UserSettings, UserTopicPreference
from app.schemas.preferences import UpdatePreferencesRequest, UpdateTopicsRequest


def get_user_settings_bundle(db: Session, user: User) -> dict:
    settings = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    prefs = (
        db.query(UserTopicPreference)
        .options(joinedload(UserTopicPreference.topic))
        .filter(UserTopicPreference.user_id == user.id)
        .all()
    )
    return {
        "timezone": user.timezone,
        "briefing_length_minutes": settings.briefing_length_minutes if settings else 6,
        "daily_schedule_time": settings.daily_schedule_time.isoformat() if settings else "08:00:00",
        "include_weekends": settings.include_weekends if settings else True,
        "selected_topics": [{"slug": pref.topic.slug, "priority_weight": pref.priority_weight} for pref in prefs],
    }


def update_user_preferences(db: Session, user: User, payload: UpdatePreferencesRequest) -> dict:
    settings = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    user.timezone = payload.timezone
    if settings:
        settings.briefing_length_minutes = payload.briefing_length_minutes
    db.commit()
    return get_user_settings_bundle(db, user)


def update_user_topics(db: Session, user: User, payload: UpdateTopicsRequest) -> None:
    db.query(UserTopicPreference).filter(UserTopicPreference.user_id == user.id).delete()
    db.flush()
    topics_by_slug = {topic.slug: topic for topic in db.query(Topic).all()}
    for item in payload.topics:
        topic = topics_by_slug.get(item.slug)
        if not topic:
            continue
        db.add(UserTopicPreference(user_id=user.id, topic_id=topic.id, priority_weight=item.priority_weight))
    db.commit()
