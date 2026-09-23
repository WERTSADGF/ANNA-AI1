from memory.models import MemoryType, PrivacyLevel


class MemoryPolicy:

    def should_store(
        self,
        content: str,
        memory_type: MemoryType,
        confidence: float,
        importance: float,
        privacy_level: PrivacyLevel,
    ) -> bool:

        if not content.strip():
            return False

        if confidence < 0.50:
            return False

        if importance < 0.30:
            return False

        if memory_type == MemoryType.SENSITIVE and privacy_level != PrivacyLevel.SENSITIVE:
            return False

        return True

    def can_retrieve(
        self,
        memory_type: MemoryType,
        privacy_level: PrivacyLevel,
        allow_sensitive: bool = False,
    ) -> bool:

        if memory_type == MemoryType.SENSITIVE:
            return allow_sensitive

        if privacy_level == PrivacyLevel.SENSITIVE:
            return allow_sensitive

        return True
