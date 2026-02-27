from __future__ import annotations

from application.ports import IrBuilder
from domain.ir import CapabilityFlags, IntermediateRepresentation
from domain.models import AnalysisResult


class DefaultIrBuilder(IrBuilder):
    def build(self, analysis: AnalysisResult) -> IntermediateRepresentation:
        requires_transactions = any(
            item["operation"] in {"WRITE", "MATWRITE"} for item in analysis.data_access_patterns
        )

        repositories: list[dict] = []
        if analysis.data_access_patterns:
            repositories.append(
                {
                    "name": "LegacyFileRepository",
                    "responsibility": "Encapsulate Pick BASIC file operations",
                    "operations": sorted({entry["operation"] for entry in analysis.data_access_patterns}),
                }
            )

        return IntermediateRepresentation(
            entities=analysis.entities,
            value_objects=[],
            services=[
                {
                    "name": "ModernizationOrchestrator",
                    "responsibility": "Coordinate validation, workflow execution, and repository access",
                    "inferred": True,
                }
            ],
            repositories=repositories,
            workflows=analysis.workflows,
            validations=analysis.business_rules,
            state_machines=analysis.control_flow,
            external_dependencies=analysis.infrastructure_coupling,
            capabilities=CapabilityFlags(
                requires_async=False,
                requires_transactions=requires_transactions,
                requires_repository_pattern=True,
            ),
            assumptions=analysis.assumptions,
            confidence_score=f"{analysis.confidence_score}%",
        )
