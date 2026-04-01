from app.services.providers.tts.espeak_provider import EspeakTTSProvider


def get_tts_provider():
    return EspeakTTSProvider()
