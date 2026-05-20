from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_path: str


class PredictionResponse(BaseModel):
    success: bool
    filename: str
    inference_time_ms: float
    original_width: int
    original_height: int
    mask_url: str
    overlay_url: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
