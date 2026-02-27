# Pick BASIC Modernizer

A semantic modernization compiler scaffold that follows:

`Pick BASIC -> Static Analysis -> Language-agnostic IR -> Target Emitter`

## Usage

```bash
python -m interface.cli sample.pick --program-name ORDER_ENTRY --mode ir
```

Modes:
- `ir`
- `architecture`
- `code`
- `full`

## Notes
- The current implementation is intentionally conservative and records assumptions where certainty is low.
- Python code emission is implemented as a clean-architecture skeleton.
- C#, Java, and PHP emitters are reserved and intentionally fail fast until implemented.
