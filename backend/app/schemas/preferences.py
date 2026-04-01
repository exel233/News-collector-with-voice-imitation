from pydantic import BaseModel


class TopicResponse(BaseModel):
    id: int
    slug: str
    label: str
    description: str

    model_config = {"from_attributes": True}


class TopicSelectionItem(BaseModel):
    slug: str
    priority_weight: float = 1.0


class UpdateTopicsRequest(BaseModel):
    topics: list[TopicSelectionItem]


class UserSettingsResponse(BaseModel):
    timezone: str
    briefing_length_minutes: int
    daily_schedule_time: str
    include_weekends: bool
    selected_topics: list[TopicSelectionItem]


class UpdatePreferencesRequest(BaseModel):
    timezone: str
    briefing_length_minutes: int
