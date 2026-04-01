from pathlib import Path

from app.services.providers.voice_clone.base import VoiceCloneProvider


class MockVoiceCloneProvider(VoiceCloneProvider):
    def register_voice(self, sample_path: Path) -> tuple[str | None, str]:
        # Guardrail: this interface is only for an authenticated user uploading their own authorized voice sample.
        return (None, f"Voice sample stored at {sample_path.name}. Custom cloning is not enabled in mock mode.")
