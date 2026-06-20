# Annotation Protocol

## Detection Datasets

Roboflow and Kaggle BrainTumor are used in their YOLO-format detection versions. Each annotation line follows:

```text
class_id x_center y_center width height
```

where all coordinates are normalized to the image width and height.

## BraTS 2021 Conversion Protocol

BraTS 2021 provides voxel-level segmentation masks rather than detection bounding boxes. The following conversion protocol was used:

1. Load the T1ce image volume and the corresponding segmentation mask.
2. Merge segmentation labels 1, 2, and 4 into a single binary tumor mask.
3. Iterate through axial slices.
4. Skip slices without tumor pixels.
5. For each tumor-containing slice, compute the minimum axis-aligned bounding rectangle covering all tumor pixels.
6. Save the slice as a 2D image.
7. Save the bounding box as a YOLO-format label with class `tumor`.

This conversion is used only to evaluate external MRI generalization trends and does not replace original box-level clinical detection annotations.

