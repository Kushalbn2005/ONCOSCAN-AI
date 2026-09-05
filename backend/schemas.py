from pydantic import BaseModel
from typing import Dict


class PredictionResponse(BaseModel):
    """
    Response returned by the prediction API.
    """

    prediction: str

    confidence: float

    probabilities: Dict[str, float]

    gradcam_url: str

    class_index: int


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str

    model_loaded: bool