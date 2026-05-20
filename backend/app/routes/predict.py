from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from ..config import settings
from ..inference import run_inference
from ..image_utils import validate_extension
from ..schemas import PredictionResponse


router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    validate_extension(file.filename)
    file_bytes = await file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File too large. Max size is {settings.max_upload_size_mb} MB.")

    try:
        result = run_inference(file_bytes, file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference failed: {exc}") from exc

    base_url = str(request.base_url).rstrip("/")
    return PredictionResponse(
        success=True,
        filename=result["filename"],
        inference_time_ms=result["inference_time_ms"],
        original_width=result["original_width"],
        original_height=result["original_height"],
        mask_url=f"{base_url}/outputs/{result['mask_file']}",
        overlay_url=f"{base_url}/outputs/{result['overlay_file']}",
    )
