from dataclasses import dataclass
from enum import Enum


class Language(str, Enum):
    ENGLISH = "english"
    MALAYALAM = "malayalam"
    MANGLISH = "manglish"
    MALAYALAM_ENGLISH = "malayalam+english"
    UNKNOWN = "unknown"


class LanguageSource(str, Enum):
    EXPLICIT = "explicit"
    CURRENT_INPUT = "current_input"
    USER_PREFERENCE = "user_preference"
    CONTEXT = "context"
    DEFAULT = "default"


@dataclass(frozen=True)
class LanguageSignal:
    language: Language
    confidence: float
    mixed: bool
    source: LanguageSource


@dataclass(frozen=True)
class LanguagePreference:
    preferred_language: Language | None = None


@dataclass(frozen=True)
class LanguageDecision:
    response_language: Language
    reason: str
    source: LanguageSource
    mixed_response: bool
