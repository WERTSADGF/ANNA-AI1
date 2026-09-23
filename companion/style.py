from dataclasses import dataclass


@dataclass(frozen=True)
class ConversationStyle:
    use_natural_language: bool = True
    avoid_robotic_phrases: bool = True
    avoid_unnecessary_repetition: bool = True
    adapt_to_context: bool = True
    adapt_to_user_language: bool = True
    concise_for_simple_questions: bool = True
    supportive_for_learning: bool = True


ROBOTIC_PHRASES = (
    "Certainly, I would be happy to assist you with that request.",
)


def is_robotic_phrase(text: str) -> bool:
    normalized = text.strip().lower()

    for phrase in ROBOTIC_PHRASES:
        if normalized == phrase.lower():
            return True

    return False
