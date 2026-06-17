#!/usr/bin/env python
"""Validate YOLO label files.

The script checks whether YOLO label values are in valid normalized ranges.
It does not modify labels unless --fix-clamp is explicitly provided.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def validate_file(path: Path, fix_clamp: bool = False) -> int:
    errors = 0
    fixed_lines = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 5:
            print(f"{path}:{idx}: invalid column count")
            errors += 1
            continue
        cls = parts[0]
        vals = list(map(float, parts[1:5]))
        if any(v < 0 or v > 1 for v in vals):
            print(f"{path}:{idx}: value outside [0, 1]: {vals}")
            errors += 1
            if fix_clamp:
                vals = [min(1.0, max(0.0, v)) for v in vals]
        fixed_lines.append(" ".join([cls] + [f"{v:.6f}" for v in vals]))

    if fix_clamp and fixed_lines:
        path.write_text("\n".join(fixed_lines) + "\n", encoding="utf-8")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label-dir", required=True)
    parser.add_argument("--fix-clamp", action="store_true")
    args = parser.parse_args()

    total_errors = 0
    for file in sorted(Path(args.label_dir).glob("*.txt")):
        total_errors += validate_file(file, args.fix_clamp)
    print(f"Total label errors: {total_errors}")


if __name__ == "__main__":
    main()

