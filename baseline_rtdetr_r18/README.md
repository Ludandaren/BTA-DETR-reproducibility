# RT-DETR-R18 Baseline Reproduction

This folder provides a minimal RT-DETR-R18 baseline setup used for reproducibility documentation. It is intended to reproduce the baseline detector under the unified experimental settings described in the manuscript.

The files in this folder only contain the baseline RT-DETR-R18 configuration and training/evaluation entry scripts. They do not include the proposed CAFU, LTA, or FSCM modules.

## Files

- `rtdetr-r18.yaml`: RT-DETR-R18 baseline model configuration.
- `train_rtdetr_r18.py`: training entry script.
- `val_rtdetr_r18.py`: evaluation entry script.

## Training

Prepare a YOLO-format dataset YAML file and run:

```bash
python baseline_rtdetr_r18/train_rtdetr_r18.py \
  --data /path/to/data.yaml \
  --project runs/baseline \
  --name rtdetr_r18
```

Default training settings follow the manuscript:

- input size: 640
- batch size: 8
- epochs: 200
- optimizer: AdamW
- initial learning rate: 1e-4
- weight decay: 1e-4
- cosine learning-rate schedule

## Evaluation

After training, evaluate the best checkpoint on the test split:

```bash
python baseline_rtdetr_r18/val_rtdetr_r18.py \
  --weights runs/baseline/rtdetr_r18/weights/best.pt \
  --data /path/to/data.yaml \
  --split test
```

The script prints Precision, Recall, mAP50, and mAP50:95.
