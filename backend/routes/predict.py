from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import shutil
import uuid
from pathlib import Path

from backend.dependencies import get_predictor, get_gradcam
from backend.schemas import PredictionResponse
from backend.config import UPLOAD_DIR
import traceback

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("", response_model=PredictionResponse)
@router.post("/", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    predictor=Depends(get_predictor),
    gradcam=Depends(get_gradcam)
):
    try:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        # Unique file name for uploaded image
        file_ext = Path(file.filename).suffix or ".jpg"
        unique_filename = f"{uuid.uuid4().hex[:8]}_{Path(file.filename).stem}{file_ext}"
        image_path = UPLOAD_DIR / unique_filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = predictor.predict_image(image_path)

        gradcam_filename = gradcam.generate(
            image_path=image_path,
            class_index=result["class_index"]
        )

        gradcam_url = f"/static/gradcam/{gradcam_filename}"

        return PredictionResponse(
            prediction=result["prediction"],
            confidence=float(result["confidence"]),
            probabilities={k: float(v) for k, v in result["probabilities"].items()},
            gradcam_url=gradcam_url,
            class_index=int(result["class_index"])
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))