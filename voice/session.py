from dataclasses import dataclass

from voice.models import VoiceSessionState


@dataclass
class VoiceSession:

    state: VoiceSessionState = VoiceSessionState.IDLE
    listening: bool = False
    speaking: bool = False
    interrupted: bool = False

    def start_listening(self) -> None:
        self.interrupted = False
        self.speaking = False
        self.listening = True
        self.state = VoiceSessionState.LISTENING

    def stop_listening(self) -> None:
        self.listening = False

        if not self.speaking:
            self.state = VoiceSessionState.STOPPED

    def start_processing(self) -> None:
        self.listening = False
        self.speaking = False
        self.state = VoiceSessionState.PROCESSING

    def start_speaking(self) -> None:
        self.listening = False
        self.speaking = True
        self.interrupted = False
        self.state = VoiceSessionState.SPEAKING

    def interrupt(self) -> None:
        self.speaking = False
        self.interrupted = True
        self.state = VoiceSessionState.INTERRUPTED

    def stop(self) -> None:
        self.listening = False
        self.speaking = False
        self.state = VoiceSessionState.STOPPED

    def fail(self) -> None:
        self.listening = False
        self.speaking = False
        self.state = VoiceSessionState.ERROR
