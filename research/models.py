from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from uuid import uuid4


class ClaimType(str, Enum):
    FACT = "fact"
    INFERENCE = "inference"
    OPINION = "opinion"
    UNCERTAIN = "uncertain"


class ResearchMode(str, Enum):
    NORMAL = "normal"
    DEEP = "deep"


@dataclass(frozen=True)
class ResearchObjective:
    question: str
    mode: ResearchMode = ResearchMode.NORMAL


@dataclass(frozen=True)
class Source:
    url: str
    title: str
    retrieved_at: str
    publisher: str = ""
    source_type: str = "unknown"
    accessed: bool = False


@dataclass(frozen=True)
class Evidence:
    claim: str
    claim_type: ClaimType
    source_urls: tuple[str, ...] = ()
    confidence: float = 0.0
    notes: str = ""


@dataclass(frozen=True)
class ResearchFinding:
    evidence: Evidence
    supporting_sources: tuple[str, ...] = ()
    conflicting_sources: tuple[str, ...] = ()


@dataclass
class ResearchReport:
    question: str
    objective_id: str = field(default_factory=lambda: str(uuid4()))
    mode: ResearchMode = ResearchMode.NORMAL
    findings: list[ResearchFinding] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
