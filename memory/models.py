from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4


class MemoryType(str, Enum):
    WORKING = "working"
    PERSONAL = "personal"
    PROJECT = "project"
    LEARNING = "learning"
    KNOWLEDGE = "knowledge"
    EPISODIC = "episodic"
    SENSITIVE = "sensitive"
    UNCERTAIN = "uncertain"


class PrivacyLevel(str, Enum):
    NORMAL = "normal"
    PRIVATE = "private"
    SENSITIVE = "sensitive"


class MemoryStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
    FORGOTTEN = "forgotten"


@dataclass
class Memory:
    content: str
    memory_type: MemoryType
    source: str
    confidence: float
    importance: float
    privacy_level: PrivacyLevel = PrivacyLevel.NORMAL
    project_id: Optional[str] = None
    expires_at: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    status: MemoryStatus = MemoryStatus.ACTIVE
    confirmed: bool = False
