from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class LegacyProgram:
    source_code: str
    program_name: str = "UNKNOWN"


@dataclass(slots=True)
class AnalysisResult:
    entities: list[dict]
    business_rules: list[dict]
    workflows: list[dict]
    data_access_patterns: list[dict]
    control_flow: list[dict]
    infrastructure_coupling: list[dict]
    assumptions: list[str] = field(default_factory=list)
    confidence_score: int = 0
