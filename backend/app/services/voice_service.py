from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import VoiceProviderStatus
from app.models.models import User, VoiceProfile
from app.services.providers.voice_clone.factory import get_voice_clone_provider


def store_voice_sample(db: Session, user: User, file_name: str, file_bytes: bytes) -> VoiceProfile:
    media_root = Path(settings.media_dir) / "voice_samples" / str(user.id)
    media_root.mkdir(parents=True, exist_ok=True)
    target_path = media_root / file_name
    target_path.write_bytes(file_bytes)

    voice_id, notes = get_voice_clone_provider().register_voice(target_path)
    profile = VoiceProfile(
        user_id=user.id,
        provider_status=VoiceProviderStatus.custom_ready if voice_id else VoiceProviderStatus.cloning_pending,
        sample_path=str(target_path),
        provider_voice_id=voice_id,
        notes=(
            "Authorized user-owned voice sample only. Do not use this interface for public figure or third-party impersonation. "
            + notes
        ),
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
