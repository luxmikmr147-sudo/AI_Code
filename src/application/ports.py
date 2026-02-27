from __future__ import annotations

from abc import ABC, abstractmethod

from domain.ir import IntermediateRepresentation
from domain.models import AnalysisResult, LegacyProgram


class LegacyAnalyzer(ABC):
    @abstractmethod
    def analyze(self, program: LegacyProgram) -> AnalysisResult:
        raise NotImplementedError


class IrBuilder(ABC):
    @abstractmethod
    def build(self, analysis: AnalysisResult) -> IntermediateRepresentation:
        raise NotImplementedError


class TargetEmitter(ABC):
    @abstractmethod
    def emit(self, ir: IntermediateRepresentation) -> str:
        raise NotImplementedError
