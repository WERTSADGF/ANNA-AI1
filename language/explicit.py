import re

from language.models import Language, LanguageSource


def detect_explicit_language_request(
    text: str,
) -> tuple[Language | None, LanguageSource]:

    value = text.strip().lower()

    patterns = {
        Language.ENGLISH: (
            r"\b(in|use|speak|reply|respond|explain)\s+english\b",
            r"\benglish\s+(please|only)\b",
        ),
        Language.MALAYALAM: (
            r"\b(in|use|speak|reply|respond|explain)\s+malayalam\b",
            r"\bmalayalam\s+(please|only)\b",
        ),
        Language.MANGLISH: (
            r"\b(in|use|speak|reply|respond|explain)\s+manglish\b",
            r"\bmanglish\s+(please|only)\b",
        ),
    }

    for language, language_patterns in patterns.items():
        for pattern in language_patterns:
            if re.search(pattern, value):
                return language, LanguageSource.EXPLICIT

    return None, LanguageSource.EXPLICIT
