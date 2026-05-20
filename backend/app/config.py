from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    app_name: str = "Lane Detection API"
    api_prefix: str = "/api"
    model_path: Path = Path(os.getenv("MODEL_PATH", PROJECT_ROOT / "best_model.keras"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", PROJECT_ROOT / "backend" / "outputs"))
    max_upload_size_mb: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    allowed_extensions: tuple[str, ...] = (".jpg", ".jpeg", ".png")
    input_height: int = int(os.getenv("MODEL_INPUT_HEIGHT", "224"))
    input_width: int = int(os.getenv("MODEL_INPUT_WIDTH", "224"))
    cors_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
        if origin.strip()
    )


settings = Settings()
settings.output_dir.mkdir(parents=True, exist_ok=True)
