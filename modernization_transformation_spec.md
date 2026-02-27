# Legacy Pick BASIC Modernization Transformation Spec

## Purpose
This document defines a semantic modernization workflow for transforming legacy Pick BASIC systems into modern, production-grade architectures without line-by-line translation.

## Core Transformation Pipeline
1. **Pick BASIC parsing and semantic analysis**
2. **Language-agnostic intermediate representation (IR) generation**
3. **Target language emission (C#, Java, Python, PHP)**

## Phase 1 — Static Analysis Requirements
Extract and reconstruct:
- Business entities (fields, inferred data types, relationships, dynamic array normalization)
- Business rules (validation, calculations, branching, state transitions, authorization when present)
- Workflows (process flow, user interactions, data lifecycle, external interactions)
- Data access patterns (READ/WRITE/MATREAD/MATWRITE semantics, locking, transactions)
- Control flow reconstruction (labels/GOTO to structured flow and state machines)
- Infrastructure coupling (screen I/O, inline DB logic, global state, external calls)

Ambiguities must be listed under assumptions. No guessing.

## Phase 2 — Legacy Decomposition
Refactor concerns into:
- Domain logic
- Application orchestration
- Infrastructure

Legacy constructs must be transformed:
- `GOTO` to structured control flow
- Implicit variables to explicit typed variables
- Dynamic arrays to typed collections
- Inline persistence to repositories
- Screen I/O to interface adapters
- Globals to dependency-injected services
- Inline validation to validation components

## Phase 3 — Language-Agnostic IR
IR output schema:

```json
{
  "entities": [],
  "value_objects": [],
  "services": [],
  "repositories": [],
  "workflows": [],
  "validations": [],
  "state_machines": [],
  "external_dependencies": [],
  "capabilities": {
    "requires_async": false,
    "requires_transactions": false,
    "requires_repository_pattern": true
  },
  "assumptions": [],
  "confidence_score": "0-100%"
}
```

Constraints:
- No fabricated business meaning
- Conservative type inference
- Explicit separation of domain and infrastructure responsibilities
- Mark inferred elements explicitly
- Include confidence score

## Phase 4 — Target Language Emission
Required architecture layers:
1. Domain
2. Application
3. Infrastructure
4. API/Interface

Design constraints:
- Clean Architecture and SOLID
- Repository pattern and DI
- DTO separation
- Error handling and logging abstractions
- Async/await where supported
- Strict typing for strongly typed languages
- Type hints for dynamically typed languages when possible
- No static/global state

## Output Modes
- **IR only**: return only valid IR JSON.
- **Architecture only**: return layered architecture design.
- **Code only**: return production-ready implementation.
- **Full transformation**: analysis summary + IR + architecture + code.

## Guardrails
- Preserve business intent, not syntax.
- Do not hallucinate missing logic/schema/UI behavior.
- Declare uncertainty explicitly.
- Never embed persistence concerns inside domain models.

## Extensibility
The IR must remain language-neutral and independent from emitter implementation. New language emitters must be addable without IR schema changes.
