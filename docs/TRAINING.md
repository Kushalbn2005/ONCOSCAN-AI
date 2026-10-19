# Training and evaluation

## Pipeline

```bash
python validate_dataset.py
python run_preprocessor.py
python run_train.py
python run_evaluate.py
```

| Script | Module | Purpose |
|--------|--------|---------|
| `run_preprocessor.py` | `ml/preprocess.py` | RGB + resize 224×224 → `data/processed` |
| `run_dataset.py` | `ml/dataset.py` | Load TF datasets (sanity check) |
| `run_model.py` | `ml/model.py` | Print EfficientNetB0 classifier summary |
| `run_train.py` | `ml/train.py` | Fit 20 epochs, batch 32 |
| `run_evaluate.py` | `ml/evaluate.py` | Test loss/accuracy, report, confusion matrix |

## Data loading

`DatasetLoader` uses `keras.utils.image_dataset_from_directory`:

- Train/val split: 20% of `data/processed/Training`, seed 42
- Test: `data/processed/Testing`, `shuffle=False`
- Cast to `float32` **without** `/255` (EfficientNetB0 already has `Rescaling(1/255)`)
- Train-only augment: horizontal flip, small rotation, zoom, contrast
- Cache **before** augment so each epoch still gets new transforms
- `prefetch(AUTOTUNE)`

If you divide by 255 in the loader, the backbone sees near-zero pixels and accuracy stalls around chance (~0.25–0.45). That was the original training bug.

## Trainer callbacks

`ml/train.py` writes:

- Best checkpoint: `artifacts/models/best_model.keras` (`val_accuracy`, max)
- Early stopping: `val_loss`, patience 5, restore best weights
- Reduce LR: `val_loss`, factor 0.2, patience 2
- CSV: `artifacts/history/training_history.csv`
- TensorBoard: `artifacts/tensorboard/`

Default run: 20 epochs, batch size 32. Change these in `run_train.py`.

`BrainTumorClassifier(fine_tune=False)` keeps the backbone frozen. After a good head-only run you can set `fine_tune=True` and a lower learning rate for a second stage (not wired in `run_train.py` yet).

## Evaluation

```bash
python run_evaluate.py
```

Writes:

- `artifacts/evaluation/metrics.json`
- `artifacts/evaluation/classification_report.txt`
- `artifacts/evaluation/confusion_matrix.png`

Latest recorded test metrics:

| Class | Precision | Recall | F1 |
|-------|-----------|--------|----|
| glioma | 0.925 | 0.740 | 0.822 |
| meningioma | 0.868 | 0.808 | 0.837 |
| notumor | 0.920 | 1.000 | 0.958 |
| pituitary | 0.839 | 0.993 | 0.910 |
| **overall accuracy** | | | **0.885** |

Glioma recall is the weakest class; inspect Grad-CAM on missed gliomas when debugging.

## TensorBoard

```bash
tensorboard --logdir artifacts/tensorboard
```
