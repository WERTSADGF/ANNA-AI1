from typing import Protocol

from voice.models import (
    SpeechOutput,
    VoiceCapabilities,
    VoiceConfig,
    VoiceLanguage,
)


class TextToSpeechProvider(Protocol):

    @property
    def provider_name(self) -> str:
        ...

    def capabilities(self) -> VoiceCapabilities:
        ...

    def synthesize(
        self,
        text: str,
        language: VoiceLanguage,
        config: VoiceConfig,
    ) -> SpeechOutput:
        ...


class MockTextToSpeechProvider:

    @property
    def provider_name(self) -> str:
        return "mock-tts"

    def capabilities(self) -> VoiceCapabilities:
        return VoiceCapabilities(
            stt=False,
            tts=True,
            streaming=False,
            interruption=True,
            malayalam=False,
            manglish=False,
            custom_voice=False,
        )

    def synthesize(
        self,
        text: str,
        language: VoiceLanguage,
        config: VoiceConfig,
    ) -> SpeechOutput:

        return SpeechOutput(
            text=text,
            language=language,
            audio_available=False,
            provider=self.provider_name,
            voice_profile_id=config.voice_profile_id,
        )
