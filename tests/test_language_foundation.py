import unittest

from language.context import build_language_context
from language.detector import detect_language
from language.models import (
    Language,
    LanguagePreference,
    LanguageSource,
)
from language.resolver import resolve_response_language


class TestLanguageFoundation(unittest.TestCase):

    def test_english(self):
        result = detect_language(
            "Please explain Python simply."
        )

        self.assertEqual(
            result.language,
            Language.ENGLISH,
        )

    def test_malayalam_script(self):
        result = detect_language(
            "എനിക്ക് ഇത് മനസ്സിലായില്ല"
        )

        self.assertEqual(
            result.language,
            Language.MALAYALAM,
        )

    def test_manglish(self):
        result = detect_language(
            "Anna ithu simple ayi explain cheyyu"
        )

        self.assertEqual(
            result.language,
            Language.MANGLISH,
        )

    def test_malayalam_english_mixed(self):
        result = detect_language(
            "ഇത് simple ആയി explain ചെയ്യൂ"
        )

        self.assertEqual(
            result.language,
            Language.MALAYALAM_ENGLISH,
        )

        self.assertTrue(result.mixed)

    def test_explicit_english_over_input(self):
        decision = resolve_response_language(
            "Malayalam il parayu, but respond in English please."
        )

        self.assertEqual(
            decision.response_language,
            Language.ENGLISH,
        )

        self.assertEqual(
            decision.source,
            LanguageSource.EXPLICIT,
        )

    def test_explicit_malayalam(self):
        decision = resolve_response_language(
            "Please explain this in Malayalam."
        )

        self.assertEqual(
            decision.response_language,
            Language.MALAYALAM,
        )

    def test_explicit_manglish(self):
        decision = resolve_response_language(
            "Reply in Manglish please."
        )

        self.assertEqual(
            decision.response_language,
            Language.MANGLISH,
        )

    def test_current_input_has_priority_over_preference(self):
        preference = LanguagePreference(
            preferred_language=Language.MALAYALAM,
        )

        decision = resolve_response_language(
            user_text="Please explain Python.",
            preference=preference,
        )

        self.assertEqual(
            decision.response_language,
            Language.ENGLISH,
        )

        self.assertEqual(
            decision.source,
            LanguageSource.CURRENT_INPUT,
        )

    def test_preference_used_for_unknown_input(self):
        preference = LanguagePreference(
            preferred_language=Language.MALAYALAM,
        )

        decision = resolve_response_language(
            user_text="12345",
            preference=preference,
        )

        self.assertEqual(
            decision.response_language,
            Language.MALAYALAM,
        )

        self.assertEqual(
            decision.source,
            LanguageSource.USER_PREFERENCE,
        )

    def test_previous_context_used_when_unknown(self):
        from language.models import LanguageSignal

        previous = LanguageSignal(
            language=Language.MANGLISH,
            confidence=0.90,
            mixed=False,
            source=LanguageSource.CURRENT_INPUT,
        )

        decision = resolve_response_language(
            user_text="12345",
            previous_language=previous,
        )

        self.assertEqual(
            decision.response_language,
            Language.MANGLISH,
        )

        self.assertEqual(
            decision.source,
            LanguageSource.CONTEXT,
        )

    def test_default_language(self):
        decision = resolve_response_language(
            user_text="12345",
        )

        self.assertEqual(
            decision.response_language,
            Language.ENGLISH,
        )

        self.assertEqual(
            decision.source,
            LanguageSource.DEFAULT,
        )

    def test_context_builder(self):
        context = build_language_context(
            user_text="Anna innu entha cheyyanam"
        )

        self.assertEqual(
            context.current_input.language,
            Language.MANGLISH,
        )

        self.assertEqual(
            context.decision.response_language,
            Language.MANGLISH,
        )


if __name__ == "__main__":
    unittest.main()
