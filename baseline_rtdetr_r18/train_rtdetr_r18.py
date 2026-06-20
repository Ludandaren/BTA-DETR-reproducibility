#!/usr/bin/env python
"""Train the RT-DETR-R18 baseline under the manuscript settings."""

from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import RTDETR


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Train RT-DETR-R18 baseline.")
    parser.add_argument("--data", required=True, help="Path to a YOLO-format dataset YAML file.")
    parser.add_argument("--model", default=str(here / "rtdetr-r18.yaml"), help="Path to RT-DETR-R18 YAML.")
    parser.add_argument("--imgsz", type=int, default=640, help="Input image size.")
    parser.add_argument("--epochs", type=int, default=200, help="Number of training epochs.")
    parser.add_argument("--batch", type=int, default=8, help="Batch size.")
    parser.add_argument("--workers", type=int, default=8, help="Number of dataloader workers.")
    parser.add_argument("--optimizer", default="AdamW", help="Optimizer name.")
    parser.add_argument("--lr0", type=float, default=1e-4, help="Initial learning rate.")
    parser.add_argument("--weight-decay", type=float, default=1e-4, help="Weight decay.")
    parser.add_argument("--project", default="runs/baseline", help="Output project directory.")
    parser.add_argument("--name", default="rtdetr_r18", help="Run name.")
    parser.add_argument("--device", default=None, help="Device id, for example '0'.")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for this run.")
    parser.add_argument("--cache", action="store_true", help="Cache dataset images during training.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = RTDETR(args.model)
    train_kwargs = {
        "data": args.data,
        "imgsz": args.imgsz,
        "epochs": args.epochs,
        "batch": args.batch,
        "workers": args.workers,
        "optimizer": args.optimizer,
        "lr0": args.lr0,
        "weight_decay": args.weight_decay,
        "cos_lr": True,
        "project": args.project,
        "name": args.name,
        "seed": args.seed,
        "cache": args.cache,
    }
    if args.device is not None:
        train_kwargs["device"] = args.device
    model.train(**train_kwargs)


if __name__ == "__main__":
    main()
