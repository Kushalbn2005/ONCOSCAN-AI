from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.dependencies import get_predictor, get_gradcam
from backend.routes.health import router as health_router
from backend.routes.predict import router as predict_router
from backend.config import GRADCAM_DIR, UPLOAD_DIR, ARTIFACTS_DIR

app = FastAPI(
    title="OncoScan AI",
    description="Brain Tumor Detection using EfficientNetB0 and Grad-CAM",
    version="1.0.0"
)

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file directories for Grad-CAM overlays and uploads
GRADCAM_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static/gradcam", StaticFiles(directory=str(GRADCAM_DIR)), name="gradcam")
app.mount("/static/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(health_router)
app.include_router(predict_router)

@app.on_event("startup")
def startup():
    get_predictor()
    print("=" * 60)
    print(" Predictor Loaded Successfully")
    print("=" * 60)


@app.get("/")
def home():
    return {
        "project": "OncoScan AI",
        "version": "1.0.0",
        "status": "Running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }