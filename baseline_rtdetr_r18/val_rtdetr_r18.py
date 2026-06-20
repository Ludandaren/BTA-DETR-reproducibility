#!/usr/bin/env python
"""Evaluate an RT-DETR-R18 baseline checkpoint."""

from __future__ import annotations

import argparse

from ultralytics import RTDETR


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate RT-DETR-R18 baseline.")
    parser.add_argument("--weights", required=True, help="Path to the trained checkpoint, such as best.pt.")
    parser.add_argument("--data", required=True, help="Path to a YOLO-format dataset YAML file.")
    parser.add_argument("--split", default="test", choices=["train", "val", "test"], help="Dataset split.")
    parser.add_argument("--imgsz", type=int, default=640, help="Input image size.")
    parser.add_argument("--batch", type=int, default=8, help="Batch size.")
    parser.add_argument("--project", default="runs/val", help="Output project directory.")
    parser.add_argument("--name", default="rtdetr_r18", help="Run name.")
    parser.add_argument("--device", default=None, help="Device id, for example '0'.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = RTDETR(args.weights)
    val_kwargs = {
        "data": args.data,
        "split": args.split,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "project": args.project,
        "name": args.name,
    }
    if args.device is not None:
        val_kwargs["device"] = args.device

    result = model.val(**val_kwargs)
    metrics = result.results_dict
    print("RT-DETR-R18 evaluation results")
    print(f"Precision: {metrics.get('metrics/precision(B)', float('nan')):.4f}")
    print(f"Recall: {metrics.get('metrics/recall(B)', float('nan')):.4f}")
    print(f"mAP50: {metrics.get('metrics/mAP50(B)', float('nan')):.4f}")
    print(f"mAP50:95: {metrics.get('metrics/mAP50-95(B)', float('nan')):.4f}")


if __name__ == "__main__":
    main()
