from ml.predict import Predictor
from ml.gradcam import GradCAM

predictor = Predictor("artifacts/models/best_model.keras")
gradcam = GradCAM(predictor)

result = gradcam.run(
    image_path="data/raw/Testing/notumor/Te-no_25.jpg"
)

print()
print("Prediction :", result["class_name"])
print("Confidence :", f"{result['confidence']:.2%}")
print("Saved to   :", result["output_path"])
