import subprocess
from pathlib import Path

from app.services.providers.tts.base import TTSProvider


class EspeakTTSProvider(TTSProvider):
    def synthesize(self, text: str, output_path: Path) -> Path | None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["espeak", "-w", str(output_path), text],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return None
        return output_path
