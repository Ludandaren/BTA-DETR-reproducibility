# Dataset Preparation

This document describes the public dataset sources, directory preparation, preprocessing workflow, and annotation conversion rules used in the manuscript.

## Roboflow Brain Tumor Detection Dataset

The Roboflow Brain Tumor Detection Dataset was used as the main dataset for training, ablation experiments, and comparison experiments. The dataset is provided in YOLO detection format and contains two classes: `Benign` and `Malignant`.

Dataset source:

```text
https://universe.roboflow.com/tumor-nt4mq/tumor-otak-r93mk/dataset/1
```

The original dataset contains 1532 MRI images and 1529 annotated instances. The original train, validation, and test subsets contain 1072, 306, and 154 images, respectively. Data augmentation was applied only to the training set, expanding the training subset to 3216 images. Validation and test images were not augmented.

The preprocessing workflow for this dataset includes image resizing to the unified input size, label-format checking, and training-set-only augmentation. The augmentation operations include random flipping, small-angle rotation, random brightness and contrast adjustment, and Gaussian-noise perturbation. The validation and test subsets use only deterministic preprocessing.

## Kaggle BrainTumor Dataset

The Kaggle BrainTumor Dataset was used as an external multi-class brain tumor detection dataset. It contains three tumor categories: `glioma`, `meningioma`, and `pituitary`.

Dataset source:

```text
https://www.kaggle.com/datasets/pkdarabi/medical-image-dataset-brain-tumor-detection
```

The dataset contains 3064 MRI images and 3064 annotated tumor instances. The train, validation, and test subsets contain 2144, 612, and 308 images, respectively. The test subset includes 159 glioma instances, 62 meningioma instances, and 87 pituitary instances.

The same deterministic preprocessing and label-format checking procedures were applied to the validation and test subsets. Training images were processed using the same input-size setting and augmentation policy described in the manuscript.

## BraTS 2021 T1ce Dataset

BraTS 2021 was used for external validation on multi-institutional MRI data. The original data are multi-parametric MRI scans with segmentation masks. To remain consistent with the single-modality setting of this study, only the T1ce modality was used.

Dataset source:

```text
https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1
```

The original segmentation labels are:

```text
0: background
1: necrotic tumor core
2: edema or invaded tissue
4: enhancing tumor
```

Labels 1, 2, and 4 were merged into a single tumor mask. For each axial slice containing tumor pixels, the minimum bounding rectangle of the merged tumor region was generated as a detection bounding box. This conversion produced 80021 tumor-containing T1ce slices and 80021 detection instances.

To avoid data leakage, train, validation, and test splits were performed at the patient level. After conversion, the train, validation, and test subsets contained 56121, 8008, and 15892 tumor-containing slices and detection instances, respectively.

For BraTS 2021, the preprocessing workflow includes T1ce volume loading, axial-slice extraction, removal of slices without tumor pixels, min-max intensity normalization, conversion of the merged tumor mask to a bounding box, and saving the resulting 2D image-label pairs in YOLO-style detection format.
