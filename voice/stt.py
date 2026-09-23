from typing import Protocol

from voice.models import (
    SpeechInput,
    VoiceCapabilities,
    VoiceLanguage,
)


class SpeechToTextProvider(Protocol):

    @property
    def provider_name(self) -> str:
        ...

    def capabilities(self) -> VoiceCapabilities:
        ...

    def transcribe(
        self,
        audio: bytes,
        language: VoiceLanguage,
    ) -> SpeechInput:
        ...


class MockSpeechToTextProvider:

    @property
    def provider_name(self) -> str:
        return "mock-stt"

    def capabilities(self) -> VoiceCapabilities:
        return VoiceCapabilities(
            stt=True,
            tts=False,
            streaming=False,
            interruption=False,
            malayalam=False,
            manglish=False,
            custom_voice=False,
        )

    def transcribe(
        self,
        audio: bytes,
        language: VoiceLanguage,
    ) -> SpeechInput:

        return SpeechInput(
            text="[mock speech input]",
            language=language,
            confidence=1.0,
        )
