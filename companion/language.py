from dataclasses import dataclass

from language.detector import detect_language as detect_language_impl
from language.models import LanguageSignal


@dataclass(frozen=True)
class CompanionLanguageSignal:
    language: str
    confidence: float
    mixed: bool


def detect_language(text: str) -> CompanionLanguageSignal:

    signal = detect_language_impl(text)

    return CompanionLanguageSignal(
        language=signal.language.value,
        confidence=signal.confidence,
        mixed=signal.mixed,
    )
