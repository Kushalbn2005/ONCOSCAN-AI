import os
from pathlib import Path

# ================================
# Project Paths
# ================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "models" / "best_model.keras"

GRADCAM_DIR = ARTIFACTS_DIR / "gradcam"
GRADCAM_DIR.mkdir(parents=True, exist_ok=True)

UPLOAD_DIR = ARTIFACTS_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ================================
# Model Configuration
# ================================

IMAGE_SIZE = (224, 224)

CLASS_NAMES = [
    "glioma",
    "meningioma",
    "notumor",
    "pituitary",
]

# ================================
# Runtime / Deploy Settings
# ================================

DEFAULT_FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def get_cors_origins() -> list[str]:
    """
    FRONTEND_ORIGINS=comma-separated list of allowed browser origins.
    Example: https://my-app.vercel.app,http://localhost:5173
    """
    raw = os.getenv("FRONTEND_ORIGINS", "").strip()
    if not raw:
        return list(DEFAULT_FRONTEND_ORIGINS)

    origins = [origin.strip().rstrip("/") for origin in raw.split(",") if origin.strip()]
    # Always keep local Vite origins for development
    for origin in DEFAULT_FRONTEND_ORIGINS:
        if origin not in origins:
            origins.append(origin)
    return origins


def get_heatmap_mode() -> str:
    """
    Heatmap generation mode:
      - full: classic Grad-CAM (memory heavy)
      - light: last-conv activation map (safe for free Render)
      - off: skip heatmaps

    HEATMAP_MODE wins if set. ENABLE_GRADCAM=true/false maps to full/off.
    On Render, default is light. Locally, default is full.
    """
    mode = os.getenv("HEATMAP_MODE", "").strip().lower()
    if mode in {"full", "light", "off"}:
        return mode

    flag = os.getenv("ENABLE_GRADCAM")
    if flag is not None:
        return "full" if flag.strip().lower() in {"1", "true", "yes", "on"} else "off"

    if os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID"):
        return "light"
    return "full"


def is_gradcam_enabled() -> bool:
    """True when any heatmap generation is enabled (full or light)."""
    return get_heatmap_mode() != "off"
