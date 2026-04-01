from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import BriefingStatus, VoiceProviderStatus
from app.models.models import Briefing, BriefingItem, User, UserSettings, VoiceProfile
from app.services.news_pipeline import ingest_articles, rank_events_for_user
from app.services.providers.tts.factory import get_tts_provider


def get_or_create_voice_profile(db: Session, user: User) -> VoiceProfile:
    profile = db.query(VoiceProfile).filter(VoiceProfile.user_id == user.id).order_by(VoiceProfile.id.desc()).first()
    if profile:
        return profile
    profile = VoiceProfile(user_id=user.id, provider_status=VoiceProviderStatus.standard, notes="Using standard TTS.")
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def build_briefing_script(user: User, ranked_events: list[dict], length_minutes: int) -> tuple[str, list[dict]]:
    max_items = max(4, min(10, length_minutes + 2))
    focus_budget = max(1, round(max_items * settings.briefing_focus_ratio))
    general_budget = max(1, max_items - focus_budget)
    focus_items = [item for item in ranked_events if item["is_focus"]][:focus_budget]
    general_items = [item for item in ranked_events if not item["is_focus"]][:general_budget]
    merged = focus_items + general_items

    if ranked_events and ranked_events[0]["event"].global_importance >= 0.93 and ranked_events[0] not in merged:
        merged = [ranked_events[0], *merged[:-1]]

    opening = "Here is your personalized AI news briefing. I will start with your focus topics, then the major headlines you should still know."
    focus_lines = ["Your focus topics:"]
    general_lines = ["Major headlines you should still know:"]
    structured_items: list[dict] = []
    focus_rank = 1
    general_rank = 1

    for item in merged:
        event = item["event"]
        line = f"{event.title}. {event.summary} {event.why_it_matters}"
        if item["is_focus"]:
            focus_lines.append(line)
            section = "focus_topics"
            rank = focus_rank
            focus_rank += 1
        else:
            general_lines.append(line)
            section = "major_headlines"
            rank = general_rank
            general_rank += 1
        structured_items.append(
            {
                "event_title": event.title,
                "section": section,
                "rank": rank,
                "summary": event.summary,
                "why_it_matters": event.why_it_matters,
                "topic_slug": event.topic_slug,
                "score": item["score"],
                "article_urls": event.metadata_json.get("article_urls", []),
            }
        )

    closing = "That wraps up your briefing. You can generate a fresh update anytime for the latest changes."
    return "\n\n".join([opening, *focus_lines, *general_lines, closing]), structured_items


def synthesize_audio(briefing: Briefing) -> str | None:
    media_root = Path(settings.media_dir)
    media_root.mkdir(parents=True, exist_ok=True)
    output_path = media_root / f"{briefing.id}.wav"
    created = get_tts_provider().synthesize(briefing.script, output_path)
    if not created:
        return None
    return f"/api/briefings/media/{output_path.name}"


def generate_briefing_for_user(db: Session, user: User, mode: str = "on_demand") -> Briefing:
    ingest_articles(db)
    user_settings = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    length_minutes = user_settings.briefing_length_minutes if user_settings else settings.default_briefing_length_minutes
    ranked = rank_events_for_user(db, user)
    script, structured_items = build_briefing_script(user, ranked, length_minutes)

    briefing = Briefing(
        user_id=user.id,
        title=f"{datetime.utcnow():%Y-%m-%d} Daily Briefing",
        script=script,
        status=BriefingStatus.pending,
        generation_mode=mode,
        metadata_json={
            "focus_ratio": settings.briefing_focus_ratio,
            "general_ratio": settings.briefing_general_ratio,
            "ranking_formula": "final_score = a*topic_relevance + b*global_importance + c*recency + d*source_diversity + e*novelty",
        },
    )
    db.add(briefing)
    db.flush()

    for item in structured_items:
        db.add(BriefingItem(briefing_id=briefing.id, **item))

    db.commit()
    db.refresh(briefing)
    briefing.audio_path = synthesize_audio(briefing)
    briefing.status = BriefingStatus.ready
    db.commit()
    db.refresh(briefing)
    return briefing


def list_briefings_for_user(db: Session, user: User) -> list[Briefing]:
    return db.query(Briefing).filter(Briefing.user_id == user.id).order_by(Briefing.generated_at.desc()).all()


def get_briefing_for_user(db: Session, user: User, briefing_id: str) -> Briefing | None:
    return db.query(Briefing).filter(Briefing.user_id == user.id, Briefing.id == briefing_id).first()
