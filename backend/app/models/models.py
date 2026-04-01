from datetime import datetime, time
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import BriefingStatus, VoiceProviderStatus


def default_uuid():
    return uuid4()


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    settings: Mapped["UserSettings"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    topic_preferences: Mapped[list["UserTopicPreference"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    briefings: Mapped[list["Briefing"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    voice_profiles: Mapped[list["VoiceProfile"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True)
    label: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")

    user_preferences: Mapped[list["UserTopicPreference"]] = relationship(back_populates="topic")


class UserTopicPreference(Base):
    __tablename__ = "user_topic_preferences"
    __table_args__ = (UniqueConstraint("user_id", "topic_id", name="uq_user_topic"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    priority_weight: Mapped[float] = mapped_column(Float, default=1.0)

    user: Mapped["User"] = relationship(back_populates="topic_preferences")
    topic: Mapped["Topic"] = relationship(back_populates="user_preferences")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    daily_schedule_time: Mapped[time] = mapped_column(Time, default=time(hour=8, minute=0))
    briefing_length_minutes: Mapped[int] = mapped_column(Integer, default=6)
    include_weekends: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship(back_populates="settings")


class SourceArticle(Base):
    __tablename__ = "source_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(String(120))
    title: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String(500), unique=True)
    topic_slug: Mapped[str] = mapped_column(String(64))
    published_at: Mapped[datetime] = mapped_column(DateTime)
    credibility_score: Mapped[float] = mapped_column(Float, default=0.7)
    importance_score: Mapped[float] = mapped_column(Float, default=0.5)
    normalized_hash: Mapped[str] = mapped_column(String(128), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NewsEvent(Base):
    __tablename__ = "news_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cluster_key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    title: Mapped[str] = mapped_column(Text)
    topic_slug: Mapped[str] = mapped_column(String(64))
    summary: Mapped[str] = mapped_column(Text)
    why_it_matters: Mapped[str] = mapped_column(Text, default="")
    source_count: Mapped[int] = mapped_column(Integer, default=1)
    global_importance: Mapped[float] = mapped_column(Float, default=0.5)
    recency_score: Mapped[float] = mapped_column(Float, default=0.5)
    novelty_score: Mapped[float] = mapped_column(Float, default=0.5)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Briefing(Base):
    __tablename__ = "briefings"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255))
    script: Mapped[str] = mapped_column(Text)
    audio_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[BriefingStatus] = mapped_column(Enum(BriefingStatus), default=BriefingStatus.pending)
    generation_mode: Mapped[str] = mapped_column(String(32), default="scheduled")
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)

    user: Mapped["User"] = relationship(back_populates="briefings")
    items: Mapped[list["BriefingItem"]] = relationship(back_populates="briefing", cascade="all, delete-orphan")


class BriefingItem(Base):
    __tablename__ = "briefing_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    briefing_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("briefings.id"))
    event_title: Mapped[str] = mapped_column(Text)
    section: Mapped[str] = mapped_column(String(64))
    rank: Mapped[int] = mapped_column(Integer)
    summary: Mapped[str] = mapped_column(Text)
    why_it_matters: Mapped[str] = mapped_column(Text, default="")
    topic_slug: Mapped[str] = mapped_column(String(64))
    score: Mapped[float] = mapped_column(Float, default=0.0)
    article_urls: Mapped[list] = mapped_column(JSONB, default=list)

    briefing: Mapped["Briefing"] = relationship(back_populates="items")


class VoiceProfile(Base):
    __tablename__ = "voice_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    provider_status: Mapped[VoiceProviderStatus] = mapped_column(
        Enum(VoiceProviderStatus), default=VoiceProviderStatus.standard
    )
    sample_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    provider_voice_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="voice_profiles")
