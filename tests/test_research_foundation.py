import unittest

from research.engine import ResearchEngine
from research.evidence import build_evidence
from research.extractor import SourceTextExtractor
from research.models import (
    ClaimType,
    ResearchMode,
    Source,
)
from research.planner import ResearchPlanner
from research.providers import MockSourceProvider
from research.reader import SourceReader
from research.uncertainty import UncertaintyChecker


class TestResearchFoundation(unittest.TestCase):

    def test_normal_plan(self):
        planner = ResearchPlanner()

        plan = planner.create(
            "What is Python?"
        )

        self.assertEqual(
            plan.objective.mode,
            ResearchMode.NORMAL,
        )

        self.assertEqual(
            len(plan.subquestions),
            1,
        )

    def test_deep_plan(self):
        planner = ResearchPlanner()

        plan = planner.create(
            "What is Python?",
            mode=ResearchMode.DEEP,
        )

        self.assertEqual(
            plan.objective.mode,
            ResearchMode.DEEP,
        )

        self.assertGreaterEqual(
            len(plan.subquestions),
            3,
        )

    def test_empty_question_rejected(self):
        planner = ResearchPlanner()

        with self.assertRaises(ValueError):
            planner.create("   ")

    def test_mock_provider(self):
        provider = MockSourceProvider()

        sources = provider.search(
            planner_objective()
        )

        self.assertEqual(
            len(sources),
            2,
        )

        self.assertTrue(
            all(source.accessed for source in sources)
        )

    def test_source_text_extraction(self):
        extractor = SourceTextExtractor()

        result = extractor.extract(
            "<html><body>Hello <b>ANNA</b></body></html>"
        )

        self.assertEqual(
            result,
            "Hello ANNA",
        )

    def test_source_reader_failure_is_honest(self):
        reader = SourceReader()

        result = reader.read(
            "https://example.invalid/anna-source"
        )

        self.assertFalse(
            result.success
        )

        self.assertEqual(
            result.content,
            "",
        )

        self.assertTrue(
            result.error
        )

    def test_fact_evidence(self):
        source = Source(
            url="https://example.invalid/source",
            title="Test",
            retrieved_at="TEST",
            accessed=True,
        )

        evidence = build_evidence(
            claim="Python is a programming language.",
            claim_type=ClaimType.FACT,
            sources=[source],
            confidence=0.95,
        )

        self.assertEqual(
            evidence.claim_type,
            ClaimType.FACT,
        )

        self.assertEqual(
            evidence.source_urls,
            (source.url,),
        )

    def test_uncertainty_checker(self):
        source = Source(
            url="https://example.invalid/source",
            title="Test",
            retrieved_at="TEST",
            accessed=True,
        )

        engine = ResearchEngine(
            provider=MockSourceProvider()
        )

        finding = engine.record_claim(
            claim="Possibly uncertain claim.",
            claim_type=ClaimType.UNCERTAIN,
            sources=[source],
            confidence=0.30,
        )

        warnings = UncertaintyChecker().inspect(
            [finding]
        )

        self.assertGreaterEqual(
            len(warnings),
            2,
        )

    def test_research_engine_plan_and_sources(self):
        engine = ResearchEngine(
            provider=MockSourceProvider()
        )

        plan, sources = engine.collect_sources(
            "Explain Python.",
            mode=ResearchMode.NORMAL,
        )

        self.assertEqual(
            plan.objective.question,
            "Explain Python.",
        )

        self.assertEqual(
            len(sources),
            2,
        )

    def test_report_contains_sources(self):
        provider = MockSourceProvider()
        engine = ResearchEngine(
            provider=provider
        )

        plan, sources = engine.collect_sources(
            "Explain Python."
        )

        finding = engine.record_claim(
            claim="This is a test finding.",
            claim_type=ClaimType.FACT,
            sources=sources,
            confidence=0.90,
        )

        report = engine.build_report(
            question="Explain Python.",
            sources=sources,
            findings=[finding],
        )

        self.assertEqual(
            report.question,
            "Explain Python.",
        )

        self.assertEqual(
            len(report.sources),
            2,
        )

        self.assertEqual(
            len(report.findings),
            1,
        )


def planner_objective():
    return ResearchPlanner().create(
        "Test research"
    ).objective


if __name__ == "__main__":
    unittest.main()
