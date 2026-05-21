from __future__ import annotations

import time

import cv2

from .image_utils import (
    create_masked_image,
    create_overlay,
    decode_upload,
    grayscale_to_bgr,
    postprocess_mask,
    preprocess_image,
    save_output_image,
)
from .model_loader import get_model


def run_inference(file_bytes: bytes, filename: str) -> dict:
    model = get_model()
    image_bgr = decode_upload(file_bytes)
    original_height, original_width = image_bgr.shape[:2]

    model_input = preprocess_image(image_bgr)

    started = time.perf_counter()
    prediction = model.predict(model_input, verbose=0)
    inference_time_ms = (time.perf_counter() - started) * 1000

    mask = postprocess_mask(prediction[0], image_bgr.shape)
    overlay = create_overlay(image_bgr, mask)
    masked_image = create_masked_image(image_bgr, mask)

    mask_file = save_output_image(grayscale_to_bgr(mask), "mask")
    masked_image_file = save_output_image(masked_image, "masked")
    overlay_file = save_output_image(overlay, "overlay")

    return {
        "success": True,
        "filename": filename,
        "inference_time_ms": round(inference_time_ms, 2),
        "original_width": original_width,
        "original_height": original_height,
        "mask_file": mask_file,
        "masked_image_file": masked_image_file,
        "overlay_file": overlay_file,
    }
