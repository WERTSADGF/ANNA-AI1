from research.evidence import build_evidence
from research.models import (
    ClaimType,
    ResearchFinding,
    ResearchMode,
    ResearchReport,
)
from research.planner import ResearchPlanner
from research.providers import SourceProvider
from research.reader import SourceReader
from research.extractor import SourceTextExtractor
from research.uncertainty import UncertaintyChecker


class ResearchEngine:

    def __init__(
        self,
        provider: SourceProvider,
        reader: SourceReader | None = None,
        extractor: SourceTextExtractor | None = None,
    ):
        self.provider = provider
        self.reader = reader or SourceReader()
        self.extractor = extractor or SourceTextExtractor()
        self.planner = ResearchPlanner()
        self.uncertainty = UncertaintyChecker()

    def create_plan(
        self,
        question: str,
        mode: ResearchMode = ResearchMode.NORMAL,
    ):
        return self.planner.create(
            question=question,
            mode=mode,
        )

    def collect_sources(
        self,
        question: str,
        mode: ResearchMode = ResearchMode.NORMAL,
    ):
        plan = self.create_plan(
            question,
            mode,
        )

        return plan, self.provider.search(
            plan.objective
        )

    def read_source(self, url: str):
        result = self.reader.read(url)

        if not result.success:
            return result

        extracted = self.extractor.extract(
            result.content
        )

        return type(result)(
            url=result.url,
            content=extracted,
            retrieved_at=result.retrieved_at,
            success=result.success,
            error=result.error,
        )

    def build_report(
        self,
        question: str,
        sources,
        findings: list[ResearchFinding],
        mode: ResearchMode = ResearchMode.NORMAL,
    ) -> ResearchReport:

        report = ResearchReport(
            question=question,
            mode=mode,
            findings=findings,
            sources=sources,
        )

        report.uncertainties = (
            self.uncertainty.inspect(
                findings
            )
        )

        return report

    def record_claim(
        self,
        claim: str,
        claim_type: ClaimType,
        sources,
        confidence: float,
        notes: str = "",
    ):
        evidence = build_evidence(
            claim=claim,
            claim_type=claim_type,
            sources=sources,
            confidence=confidence,
            notes=notes,
        )

        return ResearchFinding(
            evidence=evidence,
            supporting_sources=tuple(
                source.url
                for source in sources
                if source.accessed
            ),
        )
