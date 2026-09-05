from fastapi import APIRouter, Depends

from backend.dependencies import get_predictor
from backend.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
@router.get("/", response_model=HealthResponse)
def health(predictor=Depends(get_predictor)):
    return HealthResponse(
        status="Healthy",
        model_loaded=predictor.model is not None
    )