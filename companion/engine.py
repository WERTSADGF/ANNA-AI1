from dataclasses import dataclass

from companion.language import LanguageSignal, detect_language
from companion.profile import CompanionProfile
from companion.response_policy import (
    ResponseGuidance,
    build_response_guidance,
)


@dataclass(frozen=True)
class CompanionContext:
    profile: CompanionProfile
    language: LanguageSignal
    guidance: ResponseGuidance


class CompanionEngine:

    def __init__(self, profile: CompanionProfile | None = None):
        self.profile = profile or CompanionProfile()

    def build_context(self, user_text: str) -> CompanionContext:
        language = detect_language(user_text)

        guidance = build_response_guidance(
            user_text=user_text,
            language_signal=language,
        )

        return CompanionContext(
            profile=self.profile,
            language=language,
            guidance=guidance,
        )
