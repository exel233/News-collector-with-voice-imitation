from abc import ABC, abstractmethod
from pathlib import Path


class VoiceCloneProvider(ABC):
    @abstractmethod
    def register_voice(self, sample_path: Path) -> tuple[str | None, str]:
        raise NotImplementedError
