from __future__ import annotations

import argparse
from pathlib import Path

from application.modernization_service import ModernizationService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pick BASIC semantic modernization compiler")
    parser.add_argument("source", type=Path, help="Path to Pick BASIC source file")
    parser.add_argument("--program-name", default="UNKNOWN")
    parser.add_argument("--target", default="python", help="python|c#|java|php")
    parser.add_argument("--mode", default="ir", help="ir|architecture|code|full")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_text = args.source.read_text(encoding="utf-8")
    service = ModernizationService()
    print(
        service.transform(
            source_code=source_text,
            program_name=args.program_name,
            target_language=args.target,
            output_mode=args.mode,
        )
    )


if __name__ == "__main__":
    main()
