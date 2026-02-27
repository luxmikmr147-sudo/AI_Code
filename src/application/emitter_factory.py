from __future__ import annotations

from application.ports import TargetEmitter
from infrastructure.emitters import (
    JsonIrEmitter,
    PythonCleanArchitectureEmitter,
    UnsupportedLanguageEmitter,
)


def build_emitter(target: str, output_mode: str) -> TargetEmitter:
    if output_mode == "ir":
        return JsonIrEmitter()

    normalized = target.lower()
    if normalized == "python":
        return PythonCleanArchitectureEmitter()

    if normalized in {"c#", "java", "php"}:
        return UnsupportedLanguageEmitter(target)

    return UnsupportedLanguageEmitter(target)
