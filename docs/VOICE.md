# ANNA AI Voice Foundation

## Required Architecture

MIC
-> VOICE ACTIVITY DETECTION
-> SPEECH-TO-TEXT
-> LANGUAGE / INTENT
-> ANNA
-> RESPONSE TEXT
-> TEXT NORMALIZATION / PRONUNCIATION CONTROL
-> TEXT-TO-SPEECH
-> AUDIO

## Current Components

- STT provider abstraction
- TTS provider abstraction
- Voice provider adapter
- Voice configuration
- Speech text normalization
- Voice session manager
- Custom voice profile configuration
- Mock voice providers
- Voice tests

## Current Provider State

Only deterministic mock providers are connected.

The mock TTS provider intentionally reports:

- No actual audio output
- No Malayalam TTS capability
- No Manglish TTS capability
- No custom voice capability

Therefore this foundation does not claim that ANNA can currently speak.

## Malayalam Requirement

Natural Malayalam speech is a core ANNA requirement.

The final voice implementation must evaluate:

- Pronunciation
- Naturalness
- Rhythm
- Intonation
- Speed
- Clarity
- Code-switching
- Robotic artifacts

A Malayalam-capable provider must be connected and tested before the feature can be marked complete.

## Custom Voice

The architecture supports:

- Provider
- Voice profile ID
- Reference audio path
- Authorization state
- Style configuration
- Speed
- Pitch
- Emotion style

A reference recording does not automatically mean exact voice cloning.

The selected provider must expose the actual capability.

## Interruption

The session manager supports:

- Start listening
- Stop listening
- Processing
- Start speaking
- Interrupt
- Stop
- Error

The final audio implementation must cancel speaking when the owner interrupts.

## Current Limitations

Not implemented yet:

- Real microphone capture
- Real VAD
- Real STT provider
- Real TTS provider
- Natural Malayalam voice
- Kerala-style voice evaluation
- Streaming audio
- Audio playback
- Wake word
- Voice activity detection
- Actual voice cloning/reference conditioning
