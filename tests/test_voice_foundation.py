import unittest

from voice.custom_voice import (
    CustomVoiceProfile,
    validate_custom_voice_profile,
)
from voice.models import (
    VoiceConfig,
    VoiceLanguage,
    VoiceSessionState,
)
from voice.normalization import SpeechTextNormalizer
from voice.provider import VoiceProvider
from voice.service import VoiceService
from voice.session import VoiceSession


class TestVoiceFoundation(unittest.TestCase):

    def test_default_provider_is_mock(self):
        provider = VoiceProvider()

        description = provider.describe()

        self.assertEqual(
            description["stt_provider"],
            "mock-stt",
        )

        self.assertEqual(
            description["tts_provider"],
            "mock-tts",
        )

    def test_mock_stt(self):
        service = VoiceService()

        result = service.process_audio(
            audio=b"test",
            language=VoiceLanguage.ENGLISH,
        )

        self.assertEqual(
            result.text,
            "[mock speech input]",
        )

        self.assertEqual(
            result.language,
            VoiceLanguage.ENGLISH,
        )

    def test_mock_tts_does_not_claim_audio(self):
        service = VoiceService()

        result = service.speak(
            text="Hello ANNA.",
            language=VoiceLanguage.ENGLISH,
        )

        self.assertEqual(
            result.provider,
            "mock-tts",
        )

        self.assertFalse(
            result.audio_available
        )

    def test_malayalam_capability_is_not_falsely_claimed(self):
        provider = VoiceProvider()

        description = provider.describe()

        self.assertFalse(
            description["tts_malayalam"]
        )

        self.assertFalse(
            description["custom_voice"]
        )

    def test_normalizer(self):
        normalizer = SpeechTextNormalizer()

        result = normalizer.normalize(
            "hello\r\nworld",
            VoiceLanguage.ENGLISH,
        )

        self.assertEqual(
            result.normalized,
            "hello world",
        )

    def test_session_states(self):
        session = VoiceSession()

        self.assertEqual(
            session.state,
            VoiceSessionState.IDLE,
        )

        session.start_listening()

        self.assertEqual(
            session.state,
            VoiceSessionState.LISTENING,
        )

        session.start_processing()

        self.assertEqual(
            session.state,
            VoiceSessionState.PROCESSING,
        )

        session.start_speaking()

        self.assertEqual(
            session.state,
            VoiceSessionState.SPEAKING,
        )

        session.interrupt()

        self.assertEqual(
            session.state,
            VoiceSessionState.INTERRUPTED,
        )

        self.assertTrue(
            session.interrupted
        )

    def test_stop_listening(self):
        session = VoiceSession()

        session.start_listening()
        session.stop_listening()

        self.assertEqual(
            session.state,
            VoiceSessionState.STOPPED,
        )

        self.assertFalse(
            session.listening
        )

    def test_custom_voice_requires_authorization(self):
        profile = CustomVoiceProfile(
            provider="example",
            profile_id="voice-1",
            reference_audio_path="voice.wav",
            authorized=False,
        )

        self.assertFalse(
            validate_custom_voice_profile(profile)
        )

    def test_custom_voice_authorized(self):
        profile = CustomVoiceProfile(
            provider="example",
            profile_id="voice-1",
            reference_audio_path="voice.wav",
            authorized=True,
        )

        self.assertTrue(
            validate_custom_voice_profile(profile)
        )

    def test_voice_config(self):
        config = VoiceConfig(
            provider="mock",
            language=VoiceLanguage.MALAYALAM,
            voice_profile_id="profile-test",
            voice_style="warm-natural",
            voice_speed=1.0,
            voice_pitch=0.0,
            emotion_style="natural",
        )

        self.assertEqual(
            config.language,
            VoiceLanguage.MALAYALAM,
        )

        self.assertEqual(
            config.voice_profile_id,
            "profile-test",
        )


if __name__ == "__main__":
    unittest.main()
