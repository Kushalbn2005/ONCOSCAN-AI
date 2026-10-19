# Dataset

OncoScan AI expects a 4-class brain MRI folder layout (Kaggle-style “Brain Tumor MRI Dataset”).

## Classes

| Folder | Label index | Meaning |
|--------|-------------|---------|
| `glioma` | 0 | Glioma |
| `meningioma` | 1 | Meningioma |
| `notumor` | 2 | No tumor |
| `pituitary` | 3 | Pituitary tumor |

Folder names **must** match these strings. Keras `image_dataset_from_directory` sorts them alphabetically, which is how the indices above are assigned.

## Directory layout

```
data/raw/
├── Training/
│   ├── glioma/
│   ├── meningioma/
│   ├── notumor/
│   └── pituitary/
└── Testing/
    ├── glioma/
    ├── meningioma/
    ├── notumor/
    └── pituitary/
```

`data/processed/` mirrors this tree after `python run_preprocessor.py`.

## Current counts

From `artifacts/dataset_report.json`:

| Split | Per class | Total |
|-------|-----------|-------|
| Training | 1,400 | 5,600 |
| Testing | 400 | 1,600 |

The set is **balanced**. Training later splits 80/20 from `Training/` for train/validation (`seed=42`).

Raw files mix sizes and modes (many grayscale `L`). The preprocessor converts everything to RGB 224×224 JPEG/PNG. Saved processed images are **not** divided by 255.

## Validation

```bash
python validate_dataset.py
```

`ml/validator.py` checks required folders, counts files, flags non-image extensions, tries to open each image, and writes `artifacts/dataset_report.json`.

```bash
python check_dataset.py
```

Prints per-class counts under `data/processed`.

## Image formats

Accepted extensions: `.jpg`, `.jpeg`, `.png`.
