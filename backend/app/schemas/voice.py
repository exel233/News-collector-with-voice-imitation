from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class VoiceProfileResponse(BaseModel):
    id: int
    provider_status: str
    sample_path: str | None
    provider_voice_id: str | None
    notes: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AudioResponse(BaseModel):
    briefing_id: UUID
    audio_url: str | None
    fallback_mode: str
    script: str
