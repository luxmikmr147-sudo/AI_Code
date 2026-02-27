from __future__ import annotations

import json
from typing import Any

from application.emitter_factory import build_emitter
from application.ir_builder import DefaultIrBuilder
from domain.models import LegacyProgram
from infrastructure.pick_basic_analyzer import RegexPickBasicAnalyzer


class ModernizationService:
    def __init__(self) -> None:
        self._analyzer = RegexPickBasicAnalyzer()
        self._ir_builder = DefaultIrBuilder()

    def transform_with_details(
        self,
        source_code: str,
        program_name: str,
        target_language: str,
        output_mode: str,
    ) -> dict[str, Any]:
        analysis = self._analyzer.analyze(LegacyProgram(source_code=source_code, program_name=program_name))
        ir = self._ir_builder.build(analysis)

        if output_mode == "architecture":
            output = json.dumps(
                {
                    "domain": ["entities", "value_objects", "validations"],
                    "application": ["workflows", "orchestration_services"],
                    "infrastructure": ["repositories", "external_dependencies"],
                    "interface": ["api_adapters", "dto_mapping"],
                    "assumptions": ir.assumptions,
                },
                indent=2,
            )
        elif output_mode == "full":
            emitter = build_emitter("python", "code")
            output = json.dumps(
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
        else:
            emitter = build_emitter(target_language, output_mode)
            output = emitter.emit(ir)

        extracted_logic = {
            "state_machines": analysis.control_flow,
            "workflows": analysis.workflows,
            "data_access_patterns": analysis.data_access_patterns,
        }

        return {
            "output": output,
            "business_rules": analysis.business_rules,
            "logic": extracted_logic,
            "assumptions": analysis.assumptions,
            "confidence_score": f"{analysis.confidence_score}%",
        }

    def transform(
        self,
        source_code: str,
        program_name: str,
        target_language: str,
        output_mode: str,
    ) -> str:
        return self.transform_with_details(
            source_code=source_code,
            program_name=program_name,
            target_language=target_language,
            output_mode=output_mode,
        )["output"]
