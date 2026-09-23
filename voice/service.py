from voice.models import (
    SpeechInput,
    SpeechOutput,
    VoiceConfig,
    VoiceLanguage,
)
from voice.normalization import SpeechTextNormalizer
from voice.provider import VoiceProvider
from voice.session import VoiceSession


class VoiceService:

    def __init__(
        self,
        provider: VoiceProvider | None = None,
        session: VoiceSession | None = None,
    ):
        self.provider = provider or VoiceProvider()
        self.session = session or VoiceSession()
        self.normalizer = SpeechTextNormalizer()

    def begin_listening(self) -> None:
        self.session.start_listening()

    def stop_listening(self) -> None:
        self.session.stop_listening()

    def interrupt(self) -> None:
        self.session.interrupt()

    def process_audio(
        self,
        audio: bytes,
        language: VoiceLanguage,
    ) -> SpeechInput:

        self.session.start_processing()

        return self.provider.stt.transcribe(
            audio=audio,
            language=language,
        )

    def speak(
        self,
        text: str,
        language: VoiceLanguage,
        config: VoiceConfig | None = None,
    ) -> SpeechOutput:

        config = config or VoiceConfig(
            language=language
        )

        normalized = self.normalizer.normalize(
            text=text,
            language=language,
        )

        self.session.start_speaking()

        return self.provider.tts.synthesize(
            text=normalized.normalized,
            language=language,
            config=config,
        )
