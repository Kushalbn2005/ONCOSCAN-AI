from ml.predict import Predictor
from ml.gradcam import GradCAM

predictor = Predictor(
    "artifacts/models/best_model.keras"
)

gradcam = GradCAM(
    predictor
)

gradcam.run("data/raw/Testing/meningioma/Te-aug-me_4.jpg")

