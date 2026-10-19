# HTTP API

The FastAPI app lives in `backend/main.py`.

```bash
source venv/bin/activate
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Interactive docs: http://127.0.0.1:8000/docs

On startup the process loads `artifacts/models/best_model.keras`. That file must exist.

## CORS and environment

| Variable | Meaning |
|----------|---------|
| `FRONTEND_ORIGINS` | Comma-separated allowed origins. Always includes `http://localhost:5173` and `http://127.0.0.1:5173`. |
| `HEATMAP_MODE` | `full`, `light`, or `off`. |
| `ENABLE_GRADCAM` | If `HEATMAP_MODE` is unset: `true` → `full`, `false` → `off`. |
| `RENDER` / `RENDER_SERVICE_ID` | If set and no heatmap env vars, default mode is `light`. |

Local default heatmap mode is `full`. Copy `.env.example` and export variables in the shell (the backend does not auto-load a `.env` file unless you add that).

## Endpoints

### `GET /`

Service banner and endpoint list.

### `GET /health`

```json
{
  "status": "Healthy",
  "model_loaded": true,
  "gradcam_enabled": true,
  "heatmap_mode": "full"
}
```

The frontend treats `model_loaded` as the connection indicator.

### `POST /predict`

Multipart form field: **`file`** (JPEG/PNG MRI).

Success (`PredictionResponse`):

```json
{
  "prediction": "meningioma",
  "confidence": 0.91,
  "probabilities": {
    "glioma": 0.02,
    "meningioma": 0.91,
    "notumor": 0.01,
    "pituitary": 0.06
  },
  "gradcam_url": "/static/gradcam/gradcam_a1b2c3d4e5.png",
  "class_index": 1
}
```

`gradcam_url` is `null` when heatmaps are off or generation fails. Classification still succeeds in that case.

Failures return HTTP 500 with `{"detail": "..."}`.

### Static files

| Mount | Directory |
|-------|-----------|
| `/static/gradcam` | `artifacts/gradcam/` |
| `/static/uploads` | `artifacts/uploads/` |

The UI prefixes relative `gradcam_url` values with `VITE_API_BASE_URL`.

## curl example

```bash
curl -s -X POST http://127.0.0.1:8000/predict \
  -F "file=@data/processed/Testing/pituitary/Te-pi_4.jpg"
```

## Frontend wiring

```bash
cd frontend
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env
npm install
npm run dev
```

`frontend/src/App.jsx` posts `FormData` with the `file` field and renders `ScanStudio` + `DiagnosisPanel`.
