from pydantic import BaseModel, Field
from typing import Dict, Optional


class PredictionResponse(BaseModel):
    """
    Response returned by the prediction API.
    """

    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    gradcam_url: Optional[str] = Field(
        default=None,
        description="Relative Grad-CAM image URL, or null if Grad-CAM was skipped/failed",
    )
    class_index: int


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str
    model_loaded: bool
    gradcam_enabled: bool = False
