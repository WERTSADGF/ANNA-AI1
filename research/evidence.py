from research.models import (
    ClaimType,
    Evidence,
    ResearchFinding,
    Source,
)


def build_evidence(
    claim: str,
    claim_type: ClaimType,
    sources: list[Source],
    confidence: float,
    notes: str = "",
) -> Evidence:

    accessed_urls = tuple(
        source.url
        for source in sources
        if source.accessed
    )

    return Evidence(
        claim=claim,
        claim_type=claim_type,
        source_urls=accessed_urls,
        confidence=max(0.0, min(1.0, confidence)),
        notes=notes,
    )


def build_finding(
    evidence: Evidence,
    supporting_sources: list[Source],
    conflicting_sources: list[Source] | None = None,
) -> ResearchFinding:

    return ResearchFinding(
        evidence=evidence,
        supporting_sources=tuple(
            source.url
            for source in supporting_sources
            if source.accessed
        ),
        conflicting_sources=tuple(
            source.url
            for source in (conflicting_sources or [])
            if source.accessed
        ),
    )
