from datetime import datetime, time

from pydantic import BaseModel


class BriefingItemResponse(BaseModel):
    id: int
    event_title: str
    section: str
    rank: int
    summary: str
    why_it_matters: str
    topic_slug: str
    score: float
    article_urls: list[str]

    model_config = {"from_attributes": True}


class BriefingResponse(BaseModel):
    id: str
    title: str
    script: str
    audio_path: str | None
    status: str
    generation_mode: str
    generated_at: datetime
    metadata_json: dict
    items: list[BriefingItemResponse]

    model_config = {"from_attributes": True}


class BriefingListResponse(BaseModel):
    items: list[BriefingResponse]


class GenerateBriefingRequest(BaseModel):
    mode: str = "on_demand"


class ScheduleResponse(BaseModel):
    daily_schedule_time: time
    briefing_length_minutes: int
    include_weekends: bool


class UpdateScheduleRequest(BaseModel):
    daily_schedule_time: time
    briefing_length_minutes: int
    include_weekends: bool = True
