from abc import ABC, abstractmethod
from pathlib import Path


class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, output_path: Path) -> Path | None:
        raise NotImplementedError
