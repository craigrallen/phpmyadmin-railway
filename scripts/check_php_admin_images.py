#!/usr/bin/env python3
"""TECH-84: exact scoped admin image declarations; Python 3.9+, stdlib only."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
# Captured from the clean, real pre-change baseline; no configuration is loaded.
BASELINE_COMMIT = '27a894ed0d266db58a7c60d50eb9743fe77de3d6'
SCOPE = {'Dockerfile': {'sha256': '3206faff359404facb609baee21ffa2fd41d1b3284a14cff933cd2c330e12b01',
                'images': [(0,
                            'FROM phpmyadmin:5\n',
                            'FROM '
                            'phpmyadmin:latest@sha256:62a50b1419fe55b9b4c3cd6f5aed03a18f8f5b4a236f24735d76400bea75a5ff\n')]}}

DECLARATION = re.compile(
    rb"^[ \t]*(?:#[ \t]*)?(?:image:[ \t]+|FROM[ \t]+)"
    rb"(?:adminer|linuxserver/phpmyadmin|phpmyadmin(?:/phpmyadmin)?)(?=[:@\s])"
)


def check(sources):
    errors = []
    for path, spec in SCOPE.items():
        if path not in sources:
            errors.append(path + ": missing file")
            continue
        lines = sources[path].splitlines(keepends=True)
        expected_slots = {entry[0] for entry in spec["images"]}
        for number, old, new in spec["images"]:
            if number >= len(lines) or lines[number] != new.encode():
                errors.append(f"{path}:{number + 1}: expected exact approved image declaration")
        for number, line in enumerate(lines):
            if DECLARATION.match(line) and number not in expected_slots:
                errors.append(f"{path}:{number + 1}: unexpected admin image declaration")
    return errors


def read_sources():
    return {path: (ROOT / path).read_bytes()
            for path in SCOPE if (ROOT / path).is_file()}


def main():
    errors = check(read_sources())
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS: all scoped admin image declarations match approved immutable pins")
    return 0


if __name__ == "__main__":
    sys.exit(main())
