from functools import lru_cache

from ml.predict import Predictor
from ml.gradcam import GradCAM

from backend.config import MODEL_PATH


@lru_cache()
def get_predictor():

    return Predictor(
        model_path=MODEL_PATH
    )


@lru_cache()
def get_gradcam():

    predictor = get_predictor()

    return GradCAM(
        predictor
    )