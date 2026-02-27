from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class CapabilityFlags:
    requires_async: bool = False
    requires_transactions: bool = False
    requires_repository_pattern: bool = True


@dataclass(slots=True)
class IntermediateRepresentation:
    entities: list[dict[str, Any]] = field(default_factory=list)
    value_objects: list[dict[str, Any]] = field(default_factory=list)
    services: list[dict[str, Any]] = field(default_factory=list)
    repositories: list[dict[str, Any]] = field(default_factory=list)
    workflows: list[dict[str, Any]] = field(default_factory=list)
    validations: list[dict[str, Any]] = field(default_factory=list)
    state_machines: list[dict[str, Any]] = field(default_factory=list)
    external_dependencies: list[dict[str, Any]] = field(default_factory=list)
    capabilities: CapabilityFlags = field(default_factory=CapabilityFlags)
    assumptions: list[str] = field(default_factory=list)
    confidence_score: str = "0%"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
