from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import shutil
import uuid
import traceback
from pathlib import Path

from backend.dependencies import get_predictor, get_gradcam
from backend.schemas import PredictionResponse
from backend.config import UPLOAD_DIR, get_heatmap_mode

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)


@router.post("", response_model=PredictionResponse)
@router.post("/", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    predictor=Depends(get_predictor),
    gradcam=Depends(get_gradcam),
):
    try:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        file_ext = Path(file.filename or "scan.jpg").suffix or ".jpg"
        unique_filename = f"{uuid.uuid4().hex[:8]}_{Path(file.filename or 'scan').stem}{file_ext}"
        image_path = UPLOAD_DIR / unique_filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Core inference first — keep this path lean so Render stays alive
        result = predictor.predict_image(image_path)

        gradcam_url = None
        heatmap_mode = get_heatmap_mode()
        if heatmap_mode != "off":
            try:
                if heatmap_mode == "full":
                    gradcam_filename = gradcam.generate(
                        image_path=image_path,
                        class_index=result["class_index"],
                    )
                else:
                    # Lightweight activation map — safe for free-tier Render RAM
                    gradcam_filename = gradcam.generate_light(
                        image_path=image_path,
                        class_index=result["class_index"],
                    )
                gradcam_url = f"/static/gradcam/{gradcam_filename}"
            except Exception:
                # Non-fatal: return class prediction even if heatmap fails
                traceback.print_exc()
                gradcam_url = None

        return PredictionResponse(
            prediction=result["prediction"],
            confidence=float(result["confidence"]),
            probabilities={k: float(v) for k, v in result["probabilities"].items()},
            gradcam_url=gradcam_url,
            class_index=int(result["class_index"]),
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
