from dataclasses import dataclass

from companion.language import LanguageSignal, detect_language


@dataclass(frozen=True)
class ResponseGuidance:
    language: str
    tone: str
    style: str
    disclose_ai_identity_when_relevant: bool


def build_response_guidance(
    user_text: str,
    language_signal: LanguageSignal | None = None,
) -> ResponseGuidance:

    signal = language_signal or detect_language(user_text)

    tone = "warm-natural"
    style = "natural-conversational"

    if not user_text.strip():
        tone = "neutral"
        style = "minimal"

    return ResponseGuidance(
        language=signal.language,
        tone=tone,
        style=style,
        disclose_ai_identity_when_relevant=True,
    )
