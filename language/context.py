from dataclasses import dataclass

from language.models import (
    LanguageDecision,
    LanguagePreference,
    LanguageSignal,
)
from language.resolver import resolve_response_language


@dataclass(frozen=True)
class LanguageContext:
    current_input: LanguageSignal
    decision: LanguageDecision
    preference: LanguagePreference | None = None


def build_language_context(
    user_text: str,
    preference: LanguagePreference | None = None,
    previous_language: LanguageSignal | None = None,
) -> LanguageContext:

    from language.detector import detect_language

    current = detect_language(user_text)

    decision = resolve_response_language(
        user_text=user_text,
        preference=preference,
        previous_language=previous_language,
    )

    return LanguageContext(
        current_input=current,
        decision=decision,
        preference=preference,
    )
