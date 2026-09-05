from pathlib import Path

# ================================
# Project Paths
# ================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "models" / "best_model.keras"

GRADCAM_DIR = ARTIFACTS_DIR / "gradcam"

UPLOAD_DIR = ARTIFACTS_DIR / "uploads"

GRADCAM_DIR = ARTIFACTS_DIR / "gradcam"
GRADCAM_DIR.mkdir(parents=True, exist_ok=True)

# ================================
# Model Configuration
# ================================

IMAGE_SIZE = (224, 224)

CLASS_NAMES = [
    "glioma",
    "meningioma",
    "notumor",
    "pituitary"
]