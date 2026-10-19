# Architecture

OncoScan AI is a three-layer system: an offline ML pipeline, a FastAPI inference service, and a React viewer.

## Components

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  data/raw       │────▶│  ml/preprocess.py    │────▶│ data/processed  │
└─────────────────┘     └──────────────────────┘     └────────┬────────┘
                                                              │
                                                              ▼
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│ run_train.py    │────▶│  Trainer +           │────▶│ best_model.keras│
│                 │     │  BrainTumorClassifier│     └────────┬────────┘
└─────────────────┘     └──────────────────────┘              │
                                                              ▼
                       ┌───────────────────────────────────────────────┐
                       │ backend (FastAPI)                             │
                       │  Predictor  +  GradCAM                        │
                       │  GET /health   POST /predict                  │
                       │  /static/gradcam  /static/uploads             │
                       └──────────────────────┬────────────────────────┘
                                              │
                                              ▼
                       ┌───────────────────────────────────────────────┐
                       │ frontend (Vite + React)                       │
                       │  UploadSection → ScanStudio + DiagnosisPanel  │
                       └───────────────────────────────────────────────┘
```

## Model

`ml/model.py` builds `BrainTumorClassifier`:

- Backbone: Keras `EfficientNetB0` (`imagenet`, `include_top=False`)
- Frozen by default (`fine_tune=False`)
- Head: GAP → BatchNorm → Dropout(0.3) → Dense(256, ReLU, L2) → Dropout(0.2) → Dense(4, softmax)
- Loss: `sparse_categorical_crossentropy`
- Optimizer: Adam (`learning_rate=1e-3` in the builder)
- Input: `(224, 224, 3)` float pixels in **[0, 255]**

The saved graph is nested: top-level layers are `input_layer_*`, `efficientnetb0` (Functional submodel), then the head. Grad-CAM must read `top_conv` **inside** `efficientnetb0`, not via `model.get_layer("top_conv")`.

## Inference path

1. `backend/dependencies.py` caches one `Predictor` and one `GradCAM` with `@lru_cache`.
2. `POST /predict` writes the upload under `artifacts/uploads/`.
3. `Predictor.predict_image` resizes to 224×224 RGB float32 (no `/255`).
4. If heatmaps are enabled, `GradCAM.generate` (full) or `generate_light` (light) writes a PNG under `artifacts/gradcam/`.
5. The JSON response includes `prediction`, `confidence`, `probabilities`, `class_index`, and `gradcam_url`.

Heatmap failure is non-fatal: the class prediction is still returned.

## Frontend

`frontend/src/App.jsx` polls `GET /health` every 10 seconds and posts the selected file to `/predict`. `ScanStudio` overlays the heatmap URL (`API_BASE + gradcam_url`) on the local MRI preview.

API base URL: `VITE_API_BASE_URL` (no trailing slash). If unset, the UI targets the deployed Render host.

## Artifacts

| Path | Role |
|------|------|
| `artifacts/models/best_model.keras` | Best `val_accuracy` checkpoint |
| `artifacts/history/training_history.csv` | Per-epoch metrics |
| `artifacts/tensorboard/` | TensorBoard logs |
| `artifacts/evaluation/` | Test metrics, report, confusion matrix |
| `artifacts/gradcam/` | Heatmap PNGs / three-panel debug images |
| `artifacts/uploads/` | API upload copies |
| `artifacts/dataset_report.json` | Dataset QA |

## Config that is actually used

Runtime settings live in `backend/config.py` and environment variables (`FRONTEND_ORIGINS`, `HEATMAP_MODE`, `ENABLE_GRADCAM`).

`ml/config.py` holds image size / paths. `configs/config.yaml` is a stub and is **not** loaded by the trainer.
