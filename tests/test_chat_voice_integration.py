import unittest

from chat.models import ChatMessage, ChatRequest, ChatResponse
from chat.service import ChatService
from voice.models import VoiceLanguage
from voice.service import VoiceService


class RecordingProvider:

    provider_name = "recording"
    model_name = "voice-test"

    def __init__(self):
        self.requests = []

    def generate(self, request: ChatRequest) -> ChatResponse:
        self.requests.append(request)

        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content="ANNA voice response",
            ),
            provider=self.provider_name,
            model=self.model_name,
        )


class TestChatVoiceIntegration(unittest.TestCase):

    def setUp(self):
        self.provider = RecordingProvider()
        self.voice = VoiceService()

    def test_voice_round_trip_uses_chat_pipeline(self):
        service = ChatService(
            provider=self.provider,
            voice=self.voice,
        )

        speech_input, response, speech_output = (
            service.process_voice_input(
                audio=b"test-audio",
                language=VoiceLanguage.ENGLISH,
            )
        )

        self.assertEqual(
            speech_input.text,
            "[mock speech input]",
        )

        self.assertEqual(
            response.message.content,
            "ANNA voice response",
        )

        self.assertEqual(
            speech_output.text,
            "ANNA voice response",
        )

        self.assertEqual(
            speech_output.provider,
            "mock-tts",
        )

        self.assertFalse(
            speech_output.audio_available
        )

        self.assertEqual(
            len(self.provider.requests),
            1,
        )

    def test_voice_service_is_optional(self):
        service = ChatService(
            provider=self.provider,
        )

        with self.assertRaises(RuntimeError):
            service.process_voice_input(
                audio=b"test",
                language=VoiceLanguage.ENGLISH,
            )


if __name__ == "__main__":
    unittest.main()
