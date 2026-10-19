# OncoScan AI

Brain MRI classification for four classes — **glioma**, **meningioma**, **pituitary**, and **no tumor** — using **EfficientNetB0** with Grad-CAM heatmaps. The repo includes the training pipeline, a FastAPI inference service, and a React studio UI.

This project is for **research and education only**. It is not a medical device and must not be used for diagnosis or treatment.

## What it does

1. Preprocess MRI slices (RGB, 224×224).
2. Train a transfer-learning classifier on a balanced 4-class dataset.
3. Serve predictions over HTTP with class probabilities.
4. Overlay an explainability heatmap (full Grad-CAM locally, lighter activation maps on constrained hosts).
5. Display the scan, heatmap, and diagnosis in a web UI.

Latest evaluation on the held-out test set (`artifacts/evaluation/`):

| Metric | Value |
|--------|-------|
| Test accuracy | **88.5%** |
| Test loss | 0.507 |
| Test images | 1,600 (400 per class) |

## Architecture (high level)

```
MRI image  →  FastAPI /predict  →  EfficientNetB0  →  class + confidence
                                      ↓
                                 Grad-CAM / light heatmap
                                      ↓
                              React Scan Studio UI
```

Training path:

```
data/raw  →  preprocess  →  data/processed  →  train  →  artifacts/models/best_model.keras
```

Deeper write-ups live in [`docs/`](docs/README.md).

## Repository layout

```
ONCOSCAN-AI/
├── ml/                 Training, inference, Grad-CAM, dataset tools
├── backend/            FastAPI app (health, predict, static heatmaps)
├── frontend/           Vite + React UI
├── data/raw/           Original MRI folders (Training / Testing)
├── data/processed/     Resized RGB images used for training
├── artifacts/          Checkpoints, logs, evaluation, heatmaps
├── configs/            YAML stubs (not wired into training yet)
├── docs/               Architecture, dataset, training, API, Grad-CAM
├── run_*.py            CLI entry points
└── requirements.txt
```

## Requirements

- Python **3.11** (`runtime.txt`)
- Node.js 18+ (frontend)
- Trained weights at `artifacts/models/best_model.keras` for inference

## Setup

```bash
python3.11 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Optional environment (see `.env.example`):

```bash
# Comma-separated browser origins allowed to call the API
FRONTEND_ORIGINS=http://localhost:5173

# Heatmaps: full (Grad-CAM), light (activation map), off
HEATMAP_MODE=full
```

Frontend API URL:

```bash
cp frontend/.env.example frontend/.env
# VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Dataset

Expected folder names (ImageFolder style):

```
data/raw/
  Training/{glioma,meningioma,notumor,pituitary}/
  Testing/{glioma,meningioma,notumor,pituitary}/
```

Current counts: **5,600** training images (1,400 per class) and **1,600** test images (400 per class). See [docs/DATASET.md](docs/DATASET.md).

```bash
python validate_dataset.py    # QA report → artifacts/dataset_report.json
python run_preprocessor.py    # RGB + 224×224 → data/processed
python check_dataset.py       # print per-class counts
```

## Train, evaluate, explain

```bash
python run_model.py           # print architecture
python run_dataset.py         # load TF datasets
python run_train.py           # train 20 epochs, save best checkpoint
python run_evaluate.py        # test metrics, report, confusion matrix
python run_predict.py         # CLI inference + heatmap
python run_gradcam.py         # Grad-CAM on a sample MRI
```

**Important:** EfficientNetB0 already rescales by `1/255`. Training images stay in `[0, 255]`. Do not divide by 255 in `ml/dataset.py` or inference.

Checkpoints and logs:

- `artifacts/models/best_model.keras`
- `artifacts/history/training_history.csv`
- `artifacts/tensorboard/`
- `artifacts/evaluation/`

```bash
tensorboard --logdir artifacts/tensorboard
```

Full training notes: [docs/TRAINING.md](docs/TRAINING.md). Grad-CAM: [docs/GRADCAM.md](docs/GRADCAM.md).

## Run the API and UI

Backend (from repo root, with `venv` active):

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

- OpenAPI: http://127.0.0.1:8000/docs
- Health: `GET /health`
- Predict: `POST /predict` (multipart file field `file`)

Frontend:

```bash
cd frontend
npm install
npm run dev
```

The UI defaults to the deployed API unless `VITE_API_BASE_URL` points at your local server.

API details: [docs/API.md](docs/API.md).

## Example prediction response

```json
{
  "prediction": "pituitary",
  "confidence": 0.9985,
  "probabilities": {
    "glioma": 0.0002,
    "meningioma": 0.0010,
    "notumor": 0.0003,
    "pituitary": 0.9985
  },
  "gradcam_url": "/static/gradcam/gradcam_abc123.png",
  "class_index": 3
}
```

Class index order: `glioma` (0), `meningioma` (1), `notumor` (2), `pituitary` (3).

## Heatmap modes

| `HEATMAP_MODE` | Behavior |
|----------------|----------|
| `full` | Classic Grad-CAM (`GradientTape`). Default locally. |
| `light` | Mean last-conv activation map. Default on Render. |
| `off` | Classification only. |

`ENABLE_GRADCAM=true|false` still maps to `full` / `off` if `HEATMAP_MODE` is unset.

## Disclaimer

OncoScan AI is an investigational research prototype. Outputs can be wrong. A qualified clinician must interpret all imaging. Do not use this software as a substitute for professional medical advice.
