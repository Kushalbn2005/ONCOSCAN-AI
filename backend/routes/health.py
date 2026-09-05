from fastapi import APIRouter, Depends

from backend.dependencies import get_predictor
from backend.schemas import HealthResponse
from backend.config import get_heatmap_mode

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
@router.get("/", response_model=HealthResponse)
def health(predictor=Depends(get_predictor)):
    mode = get_heatmap_mode()
    return HealthResponse(
        status="Healthy",
        model_loaded=predictor.model is not None,
        gradcam_enabled=mode != "off",
        heatmap_mode=mode,
    )