from dataclasses import dataclass
from enum import Enum


class VoiceLanguage(str, Enum):
    ENGLISH = "english"
    MALAYALAM = "malayalam"
    MANGLISH = "manglish"
    MALAYALAM_ENGLISH = "malayalam+english"
    UNKNOWN = "unknown"


class VoiceSessionState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    INTERRUPTED = "interrupted"
    STOPPED = "stopped"
    ERROR = "error"


class VoiceCapability(str, Enum):
    STT = "stt"
    TTS = "tts"
    STREAMING = "streaming"
    INTERRUPTION = "interruption"
    MALAYALAM = "malayalam"
    MANGlish = "manglish"
    CUSTOM_VOICE = "custom_voice"


@dataclass(frozen=True)
class VoiceConfig:
    provider: str = "mock"
    language: VoiceLanguage = VoiceLanguage.ENGLISH
    voice_profile_id: str | None = None
    voice_style: str = "warm-natural"
    voice_speed: float = 1.0
    voice_pitch: float = 0.0
    emotion_style: str = "natural"


@dataclass(frozen=True)
class VoiceCapabilities:
    stt: bool
    tts: bool
    streaming: bool
    interruption: bool
    malayalam: bool
    manglish: bool
    custom_voice: bool


@dataclass(frozen=True)
class SpeechInput:
    text: str
    language: VoiceLanguage
    confidence: float


@dataclass(frozen=True)
class SpeechOutput:
    text: str
    language: VoiceLanguage
    audio_available: bool
    provider: str
    voice_profile_id: str | None = None
