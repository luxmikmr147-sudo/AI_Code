from __future__ import annotations

import json

from application.ports import TargetEmitter
from domain.ir import IntermediateRepresentation


class JsonIrEmitter(TargetEmitter):
    def emit(self, ir: IntermediateRepresentation) -> str:
        return json.dumps(ir.to_dict(), indent=2)


class PythonCleanArchitectureEmitter(TargetEmitter):
    def emit(self, ir: IntermediateRepresentation) -> str:
        return "\n".join(
            [
                "# Generated modernized architecture skeleton (Python)",
                "# Domain",
                "class DomainService:",
                "    pass",
                "",
                "# Application",
                "class ApplicationService:",
                "    def __init__(self, repository):",
                "        self._repository = repository",
                "",
                "# Infrastructure",
                "class Repository:",
                "    async def load(self, key: str):",
                "        raise NotImplementedError",
                "",
                "# Interface/API",
                "def handle_request(dto: dict):",
                "    return {'status': 'accepted', 'assumptions': " + repr(ir.assumptions) + "}",
            ]
        )


class UnsupportedLanguageEmitter(TargetEmitter):
    def __init__(self, language: str) -> None:
        self.language = language

    def emit(self, ir: IntermediateRepresentation) -> str:
        raise ValueError(f"Unsupported target language: {self.language}")
