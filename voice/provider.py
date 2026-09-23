from voice.models import VoiceCapabilities, VoiceConfig
from voice.stt import (
    MockSpeechToTextProvider,
    SpeechToTextProvider,
)
from voice.tts import (
    MockTextToSpeechProvider,
    TextToSpeechProvider,
)


class VoiceProvider:

    def __init__(
        self,
        stt: SpeechToTextProvider | None = None,
        tts: TextToSpeechProvider | None = None,
    ):
        self.stt = stt or MockSpeechToTextProvider()
        self.tts = tts or MockTextToSpeechProvider()

    def stt_capabilities(
        self,
    ) -> VoiceCapabilities:
        return self.stt.capabilities()

    def tts_capabilities(
        self,
    ) -> VoiceCapabilities:
        return self.tts.capabilities()

    def describe(self) -> dict:
        stt = self.stt.capabilities()
        tts = self.tts.capabilities()

        return {
            "stt_provider": self.stt.provider_name,
            "tts_provider": self.tts.provider_name,
            "stt_malayalam": stt.malayalam,
            "stt_manglish": stt.manglish,
            "tts_malayalam": tts.malayalam,
            "tts_manglish": tts.manglish,
            "custom_voice": tts.custom_voice,
            "streaming": (
                stt.streaming and tts.streaming
            ),
            "interruption": tts.interruption,
        }
