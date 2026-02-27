# Pick BASIC Modernizer

A semantic modernization compiler scaffold that follows:

`Pick BASIC -> Static Analysis -> Language-agnostic IR -> Target Emitter`

## Run CLI

```bash
PYTHONPATH=src python -m interface.cli sample.pick --program-name ORDER_ENTRY --mode ir
```

Modes:
- `ir`
- `architecture`
- `code`
- `full`

## Run Web UI (HTML)

Install dependencies:

```bash
pip install -e .
```

Start server:

```bash
PYTHONPATH=src python -m interface.web
```

Open in browser:

- http://localhost:8000

The web screen lets you:
- Paste Pick BASIC source code
- Select mode (`ir`, `architecture`, `code`, `full`)
- Select target language (`python`, `c#`, `java`, `php`)
- Convert and copy the generated output
- View extracted business rules and logic in a dedicated panel

## Test

```bash
pytest -q
```

## Notes
- The current implementation is intentionally conservative and records assumptions where certainty is low.
- Python code emission is implemented as a clean-architecture skeleton.
- C#, Java, and PHP emitters are reserved and intentionally fail fast until implemented.
