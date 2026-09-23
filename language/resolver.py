from language.detector import detect_language
from language.explicit import detect_explicit_language_request
from language.models import (
    Language,
    LanguageDecision,
    LanguagePreference,
    LanguageSignal,
    LanguageSource,
)


def resolve_response_language(
    user_text: str,
    preference: LanguagePreference | None = None,
    previous_language: LanguageSignal | None = None,
) -> LanguageDecision:

    explicit_language, explicit_source = (
        detect_explicit_language_request(user_text)
    )

    if explicit_language is not None:
        return LanguageDecision(
            response_language=explicit_language,
            reason="Explicit user language request.",
            source=explicit_source,
            mixed_response=explicit_language
            in (
                Language.MANGLISH,
                Language.MALAYALAM_ENGLISH,
            ),
        )

    current = detect_language(user_text)

    if current.language != Language.UNKNOWN:
        return LanguageDecision(
            response_language=current.language,
            reason="Current conversation language.",
            source=LanguageSource.CURRENT_INPUT,
            mixed_response=current.mixed,
        )

    if preference and preference.preferred_language:
        return LanguageDecision(
            response_language=preference.preferred_language,
            reason="Stored user language preference.",
            source=LanguageSource.USER_PREFERENCE,
            mixed_response=preference.preferred_language
            in (
                Language.MANGLISH,
                Language.MALAYALAM_ENGLISH,
            ),
        )

    if previous_language and previous_language.language != Language.UNKNOWN:
        return LanguageDecision(
            response_language=previous_language.language,
            reason="Previous conversation language.",
            source=LanguageSource.CONTEXT,
            mixed_response=previous_language.mixed,
        )

    return LanguageDecision(
        response_language=Language.ENGLISH,
        reason="Default language.",
        source=LanguageSource.DEFAULT,
        mixed_response=False,
    )
