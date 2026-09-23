import re

from language.models import (
    Language,
    LanguageSignal,
    LanguageSource,
)


MANGlish_WORDS = {
    "nammal",
    "ennu",
    "entha",
    "engane",
    "cheyyu",
    "cheyyuka",
    "parayu",
    "manassilayi",
    "manassilayilla",
    "venam",
    "illa",
    "athu",
    "ithu",
    "innale",
    "innu",
    "pinne",
    "evide",
    "enthanu",
    "nokkam",
    "padippikku",
    "padikkan",
    "ariyam",
    "ariyilla",
    "sheri",
    "athe",
    "alle",
}


def contains_malayalam_script(text: str) -> bool:
    return any(
        "\u0D00" <= character <= "\u0D7F"
        for character in text
    )


def latin_words(text: str) -> list[str]:
    return re.findall(
        r"[A-Za-z]+(?:'[A-Za-z]+)?",
        text.lower(),
    )


def detect_language(text: str) -> LanguageSignal:
    value = text.strip()

    if not value:
        return LanguageSignal(
            language=Language.UNKNOWN,
            confidence=0.0,
            mixed=False,
            source=LanguageSource.CURRENT_INPUT,
        )

    has_malayalam_script = contains_malayalam_script(value)

    words = latin_words(value)

    manglish_hits = sum(
        1
        for word in words
        if word in MANGlish_WORDS
    )

    english_markers = {
        "the",
        "this",
        "that",
        "what",
        "why",
        "how",
        "please",
        "explain",
        "teach",
        "show",
        "help",
        "project",
        "python",
        "code",
        "research",
    }

    english_hits = sum(
        1
        for word in words
        if word in english_markers
    )

    if has_malayalam_script and words:
        return LanguageSignal(
            language=Language.MALAYALAM_ENGLISH,
            confidence=0.95,
            mixed=True,
            source=LanguageSource.CURRENT_INPUT,
        )

    if has_malayalam_script:
        return LanguageSignal(
            language=Language.MALAYALAM,
            confidence=0.98,
            mixed=False,
            source=LanguageSource.CURRENT_INPUT,
        )

    if manglish_hits > 0 and english_hits > 0:
        return LanguageSignal(
            language=Language.MANGLISH,
            confidence=0.85,
            mixed=True,
            source=LanguageSource.CURRENT_INPUT,
        )

    if manglish_hits >= 2:
        return LanguageSignal(
            language=Language.MANGLISH,
            confidence=0.90,
            mixed=False,
            source=LanguageSource.CURRENT_INPUT,
        )

    if english_hits > 0 or words:
        return LanguageSignal(
            language=Language.ENGLISH,
            confidence=0.70,
            mixed=False,
            source=LanguageSource.CURRENT_INPUT,
        )

    return LanguageSignal(
        language=Language.UNKNOWN,
        confidence=0.20,
        mixed=False,
        source=LanguageSource.CURRENT_INPUT,
    )
