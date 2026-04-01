import enum


class BriefingStatus(str, enum.Enum):
    pending = "pending"
    ready = "ready"
    failed = "failed"


class VoiceProviderStatus(str, enum.Enum):
    standard = "standard"
    cloning_pending = "cloning_pending"
    custom_ready = "custom_ready"
    unavailable = "unavailable"
