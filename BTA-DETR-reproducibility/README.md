# BTA-DETR Reproducibility Package

This repository provides supplementary reproducibility materials for the manuscript on BTA-DETR for brain tumor MRI detection. It documents the dataset sources, preprocessing workflow, annotation conversion rules, public training settings, dataset-statistics scripts, and module-level pseudocode used to describe the proposed method.

## Contents

- `configs/`: dataset and training settings.
- `scripts/`: preprocessing, annotation conversion, and dataset-statistics scripts.
- `docs/`: dataset preparation, annotation protocol, module pseudocode, and code availability statement.

## Datasets

The study uses three publicly available brain tumor MRI datasets:

1. Roboflow Brain Tumor Detection Dataset
2. Kaggle BrainTumor Dataset
3. BraTS 2021 Task 1 Dataset

Users can download the public datasets from their original sources and arrange them according to the instructions in `docs/dataset_preparation.md`.

## Included Materials

This package provides:

- dataset source documentation;
- preprocessing and annotation conversion scripts;
- dataset statistics and lesion-size distribution;
- public training-setting documentation;
- module-level pseudocode documentation for CAFU, LTA, and FSCM.

## Suggested Use

Install dependencies:

```bash
pip install -r requirements.txt
```

Summarize a YOLO-format dataset:

```bash
python scripts/summarize_dataset.py --data-yaml configs/dataset_roboflow.yaml
```

Convert BraTS 2021 segmentation masks into YOLO-format detection boxes:

```bash
python scripts/convert_brats_mask_to_boxes.py --input /path/to/BraTS2021_Training_Data --output /path/to/brats_t1ce_yolo
```
