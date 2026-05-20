from __future__ import annotations

import base64
from pathlib import Path
from uuid import uuid4

import cv2
import numpy as np

from .config import settings


def validate_extension(filename: str) -> None:
    ext = Path(filename).suffix.lower()
    if ext not in settings.allowed_extensions:
        raise ValueError(
            f"Unsupported file type '{ext}'. Allowed types: {', '.join(settings.allowed_extensions)}"
        )


def decode_upload(file_bytes: bytes) -> np.ndarray:
    array = np.frombuffer(file_bytes, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Uploaded file is not a valid image.")
    return image


def preprocess_image(image_bgr: np.ndarray) -> np.ndarray:
    resized = cv2.resize(image_bgr, (settings.input_width, settings.input_height))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    normalized = rgb.astype(np.float32) / 255.0
    return np.expand_dims(normalized, axis=0)


def postprocess_mask(prediction: np.ndarray, original_shape: tuple[int, int, int]) -> np.ndarray:
    mask = np.squeeze(prediction)
    mask = np.round(mask).astype(np.uint8) * 255
    original_height, original_width = original_shape[:2]
    resized_mask = cv2.resize(mask, (original_width, original_height), interpolation=cv2.INTER_NEAREST)
    return resized_mask


def create_overlay(image_bgr: np.ndarray, mask: np.ndarray) -> np.ndarray:
    color_mask = np.zeros_like(image_bgr)
    color_mask[:, :, 1] = mask
    overlay = cv2.addWeighted(image_bgr, 1.0, color_mask, 0.45, 0)
    return overlay


def save_output_image(image_bgr: np.ndarray, suffix: str) -> str:
    filename = f"{uuid4().hex}_{suffix}.png"
    output_path = settings.output_dir / filename
    ok = cv2.imwrite(str(output_path), image_bgr)
    if not ok:
        raise RuntimeError(f"Failed to save output image: {output_path}")
    return filename


def grayscale_to_bgr(mask: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)


def image_file_to_data_url(path: Path) -> str:
    mime = "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"
