#!/usr/bin/env python
"""Summarize a YOLO-format detection dataset.

This utility reports the number of images, labels, instances per class, and
lesion-size distribution based on normalized YOLO bounding boxes.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from collections import Counter
import yaml


def read_label_file(path: Path):
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        cls = int(float(parts[0]))
        x, y, w, h = map(float, parts[1:5])
        rows.append((cls, x, y, w, h))
    return rows


def size_bucket(area: float) -> str:
    if area < 0.02:
        return "small(<2%)"
    if area < 0.10:
        return "medium(2-10%)"
    return "large(>=10%)"


def summarize_labels(label_dir: Path):
    class_counts = Counter()
    size_counts = Counter()
    label_files = sorted(label_dir.glob("*.txt"))
    total_instances = 0
    for file in label_files:
        for cls, _, _, w, h in read_label_file(file):
            total_instances += 1
            class_counts[cls] += 1
            size_counts[size_bucket(w * h)] += 1
    return {
        "label_files": len(label_files),
        "instances": total_instances,
        "class_counts": dict(class_counts),
        "size_counts": dict(size_counts),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-yaml", required=True, help="Dataset YAML or config file")
    parser.add_argument("--label-dir", default=None, help="Optional YOLO label directory")
    args = parser.parse_args()

    cfg_path = Path(args.data_yaml)
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    print(f"Dataset: {cfg.get('name', cfg_path.stem)}")
    print(f"Classes: {cfg.get('classes', {})}")

    if args.label_dir:
        summary = summarize_labels(Path(args.label_dir))
        for key, value in summary.items():
            print(f"{key}: {value}")
    else:
        print("No --label-dir provided; only configuration metadata was printed.")


if __name__ == "__main__":
    main()

