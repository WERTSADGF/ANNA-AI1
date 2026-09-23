from dataclasses import dataclass


@dataclass(frozen=True)
class CustomVoiceProfile:
    provider: str
    profile_id: str
    reference_audio_path: str | None
    authorized: bool
    notes: str = ""


def validate_custom_voice_profile(
    profile: CustomVoiceProfile,
) -> bool:

    if not profile.provider.strip():
        return False

    if not profile.profile_id.strip():
        return False

    # The application does not assume that a reference recording
    # guarantees an exact voice match. The provider must expose
    # the actual capability.
    if not profile.authorized:
        return False

    return True
