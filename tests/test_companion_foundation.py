import unittest

from companion.engine import CompanionEngine
from companion.language import detect_language
from companion.profile import CompanionProfile
from companion.response_policy import build_response_guidance
from companion.style import ConversationStyle, is_robotic_phrase


class TestCompanionFoundation(unittest.TestCase):

    def test_identity(self):
        profile = CompanionProfile()

        self.assertEqual(profile.name, "ANNA")
        self.assertEqual(profile.identity, "AI")
        self.assertTrue(profile.transparent_ai_identity)
        self.assertFalse(profile.pretend_to_be_human)
        self.assertFalse(profile.invent_memories)

    def test_roles(self):
        profile = CompanionProfile()

        self.assertEqual(
            profile.primary_role,
            "Personal AI Companion",
        )

        self.assertIn(
            "Personal AI Assistant",
            profile.secondary_roles,
        )

        self.assertIn(
            "Personal AI Tutor / Teaching Friend",
            profile.secondary_roles,
        )

    def test_english_detection(self):
        signal = detect_language("Hello Anna")

        self.assertEqual(signal.language, "english")

    def test_malayalam_detection(self):
        signal = detect_language("നമസ്കാരം")

        self.assertEqual(signal.language, "malayalam")

    def test_manglish_detection(self):
        signal = detect_language("Anna innu entha cheyyanam")

        self.assertEqual(signal.language, "manglish")

    def test_mixed_detection(self):
        signal = detect_language("Hello Anna നമസ്കാരം")

        self.assertTrue(signal.mixed)

    def test_response_guidance(self):
        guidance = build_response_guidance(
            "Anna, explain this simply."
        )

        self.assertEqual(guidance.language, "english")
        self.assertEqual(guidance.tone, "warm-natural")
        self.assertEqual(guidance.style, "natural-conversational")
        self.assertTrue(guidance.disclose_ai_identity_when_relevant)

    def test_engine_context(self):
        engine = CompanionEngine()

        context = engine.build_context(
            "Anna innu entha cheyyanam"
        )

        self.assertEqual(context.profile.name, "ANNA")
        self.assertEqual(context.language.language, "manglish")

    def test_style_rules(self):
        style = ConversationStyle()

        self.assertTrue(style.use_natural_language)
        self.assertTrue(style.avoid_robotic_phrases)

    def test_robotic_phrase_detection(self):
        self.assertTrue(
            is_robotic_phrase(
                "Certainly, I would be happy to assist you with that request."
            )
        )

        self.assertFalse(
            is_robotic_phrase(
                "Okay, nammal nokkam."
            )
        )


if __name__ == "__main__":
    unittest.main()
