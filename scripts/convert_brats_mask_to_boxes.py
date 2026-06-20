#!/usr/bin/env python
"""Convert BraTS 2021 segmentation masks into YOLO-format detection boxes.

This script merges BraTS labels 1, 2, and 4 into one tumor mask and generates
one bounding box for each axial slice containing tumor pixels.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import nibabel as nib
import numpy as np
from PIL import Image
from tqdm import tqdm


def normalize_to_uint8(slice_2d: np.ndarray) -> np.ndarray:
    arr = slice_2d.astype(np.float32)
    lo, hi = np.percentile(arr, [1, 99])
    arr = np.clip(arr, lo, hi)
    if hi > lo:
        arr = (arr - lo) / (hi - lo)
    else:
        arr = np.zeros_like(arr)
    return (arr * 255).astype(np.uint8)


def mask_to_yolo_box(mask: np.ndarray):
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return None
    x1, x2 = xs.min(), xs.max()
    y1, y2 = ys.min(), ys.max()
    h, w = mask.shape
    xc = ((x1 + x2 + 1) / 2) / w
    yc = ((y1 + y2 + 1) / 2) / h
    bw = (x2 - x1 + 1) / w
    bh = (y2 - y1 + 1) / h
    return 0, xc, yc, bw, bh


def process_patient(patient_dir: Path, output_dir: Path):
    patient_id = patient_dir.name
    t1ce_files = list(patient_dir.glob("*_t1ce.nii.gz")) + list(patient_dir.glob("*_t1ce.nii"))
    seg_files = list(patient_dir.glob("*_seg.nii.gz")) + list(patient_dir.glob("*_seg.nii"))
    if not t1ce_files or not seg_files:
        return 0

    image_vol = nib.load(str(t1ce_files[0])).get_fdata()
    seg_vol = nib.load(str(seg_files[0])).get_fdata()

    image_dir = output_dir / "images"
    label_dir = output_dir / "labels"
    image_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for z in range(seg_vol.shape[2]):
        tumor = np.isin(seg_vol[:, :, z], [1, 2, 4])
        box = mask_to_yolo_box(tumor)
        if box is None:
            continue

        img = normalize_to_uint8(image_vol[:, :, z])
        stem = f"{patient_id}_slice_{z:03d}"
        Image.fromarray(img).save(image_dir / f"{stem}.png")
        cls, xc, yc, bw, bh = box
        (label_dir / f"{stem}.txt").write_text(
            f"{cls} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n",
            encoding="utf-8",
        )
        written += 1
    return written


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="BraTS2021_Training_Data directory")
    parser.add_argument("--output", required=True, help="Output YOLO-format directory")
    args = parser.parse_args()

    root = Path(args.input)
    out = Path(args.output)
    patients = sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("BraTS2021_"))

    total = 0
    for p in tqdm(patients, desc="Converting BraTS"):
        total += process_patient(p, out)
    print(f"Converted tumor-containing slices: {total}")


if __name__ == "__main__":
    main()

