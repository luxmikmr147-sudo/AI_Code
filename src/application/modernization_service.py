from __future__ import annotations

import json

from application.emitter_factory import build_emitter
from application.ir_builder import DefaultIrBuilder
from domain.models import LegacyProgram
from infrastructure.pick_basic_analyzer import RegexPickBasicAnalyzer


class ModernizationService:
    def __init__(self) -> None:
        self._analyzer = RegexPickBasicAnalyzer()
        self._ir_builder = DefaultIrBuilder()

    def transform(
        self,
        source_code: str,
        program_name: str,
        target_language: str,
        output_mode: str,
    ) -> str:
        analysis = self._analyzer.analyze(LegacyProgram(source_code=source_code, program_name=program_name))
        ir = self._ir_builder.build(analysis)

        if output_mode == "architecture":
            architecture = {
                "domain": ["entities", "value_objects", "validations"],
                "application": ["workflows", "orchestration_services"],
                "infrastructure": ["repositories", "external_dependencies"],
                "interface": ["api_adapters", "dto_mapping"],
                "assumptions": ir.assumptions,
            }
            return json.dumps(architecture, indent=2)

        if output_mode == "full":
            emitter = build_emitter("python", "code")
            return json.dumps(
                {
                    "analysis_summary": {
                        "rules": len(analysis.business_rules),
                        "data_access_patterns": len(analysis.data_access_patterns),
                        "assumptions": analysis.assumptions,
                    },
                    "ir": ir.to_dict(),
                    "architecture": {
                        "layers": ["domain", "application", "infrastructure", "interface"]
                    },
                    "code": emitter.emit(ir),
                },
                indent=2,
            )

        emitter = build_emitter(target_language, output_mode)
        return emitter.emit(ir)
