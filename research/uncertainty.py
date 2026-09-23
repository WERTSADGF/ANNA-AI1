from research.models import ResearchFinding


class UncertaintyChecker:

    def inspect(
        self,
        findings: list[ResearchFinding],
    ) -> list[str]:

        warnings = []

        for finding in findings:

            evidence = finding.evidence

            if evidence.claim_type.value == "uncertain":
                warnings.append(
                    f"Uncertain claim: {evidence.claim}"
                )

            if evidence.confidence < 0.50:
                warnings.append(
                    f"Low-confidence claim: {evidence.claim}"
                )

            if (
                finding.supporting_sources
                and finding.conflicting_sources
            ):
                warnings.append(
                    f"Conflicting sources for claim: "
                    f"{evidence.claim}"
                )

        return warnings
