from dataclasses import dataclass

from voice.models import VoiceLanguage


@dataclass(frozen=True)
class NormalizedSpeechText:
    original: str
    normalized: str
    language: VoiceLanguage


class SpeechTextNormalizer:

    def normalize(
        self,
        text: str,
        language: VoiceLanguage,
    ) -> NormalizedSpeechText:

        normalized = " ".join(
            text.replace("\r\n", "\n")
                .replace("\r", "\n")
                .split()
        )

        return NormalizedSpeechText(
            original=text,
            normalized=normalized,
            language=language,
        )
