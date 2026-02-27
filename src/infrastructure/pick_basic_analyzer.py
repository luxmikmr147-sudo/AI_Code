from __future__ import annotations

import re

from application.ports import LegacyAnalyzer
from domain.models import AnalysisResult, LegacyProgram

READ_OPS = ("READ", "WRITE", "MATREAD", "MATWRITE")


class RegexPickBasicAnalyzer(LegacyAnalyzer):
    """Conservative static analyzer for Pick BASIC.

    This analyzer only extracts explicit signals present in the source code and
    records assumptions for ambiguous constructs.
    """

    def analyze(self, program: LegacyProgram) -> AnalysisResult:
        source = program.source_code
        lines = [line.rstrip() for line in source.splitlines() if line.strip()]

        entities: list[dict] = []
        business_rules: list[dict] = []
        workflows: list[dict] = []
        data_access_patterns: list[dict] = []
        control_flow: list[dict] = []
        infrastructure_coupling: list[dict] = []
        assumptions: list[str] = []

        labels = [line[:-1] for line in lines if line.endswith(":")]
        if labels:
            control_flow.append(
                {
                    "pattern": "label_driven",
                    "labels": labels,
                    "recommendation": "refactor labels/GOTO into structured loops and conditionals",
                }
            )

        for line in lines:
            upper = line.upper()

            if "GOTO" in upper:
                control_flow.append(
                    {
                        "pattern": "goto",
                        "raw": line,
                        "recommendation": "replace with structured branching",
                    }
                )

            if upper.startswith("IF "):
                business_rules.append(
                    {
                        "type": "conditional_rule",
                        "expression": line,
                        "inferred": False,
                    }
                )

            for op in READ_OPS:
                if re.search(rf"\b{op}\b", upper):
                    data_access_patterns.append(
                        {
                            "operation": op,
                            "raw": line,
                            "lock_semantics": "unknown",
                        }
                    )

            if "CRT" in upper or "INPUT" in upper:
                infrastructure_coupling.append(
                    {
                        "type": "screen_io",
                        "raw": line,
                    }
                )

            if "CALL " in upper:
                infrastructure_coupling.append(
                    {
                        "type": "external_call",
                        "raw": line,
                    }
                )

            if "<" in line and ">" in line:
                assumptions.append(
                    "Detected dynamic-array-style indexing; exact schema unknown and requires domain confirmation."
                )

        if not entities:
            assumptions.append("No explicit entity definitions found in source; entity reconstruction requires data dictionary or file metadata.")

        confidence = 60
        if assumptions:
            confidence -= min(len(assumptions) * 5, 30)

        workflows.append(
            {
                "name": program.program_name,
                "steps": ["load program", "evaluate rules", "perform data I/O as declared"],
                "inferred": True,
            }
        )

        return AnalysisResult(
            entities=entities,
            business_rules=business_rules,
            workflows=workflows,
            data_access_patterns=data_access_patterns,
            control_flow=control_flow,
            infrastructure_coupling=infrastructure_coupling,
            assumptions=sorted(set(assumptions)),
            confidence_score=max(confidence, 10),
        )
