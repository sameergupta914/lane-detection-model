from __future__ import annotations

from functools import lru_cache

import tensorflow as tf
from tensorflow.keras import backend as K

from .config import settings


def dice_coefficient(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    mu = y_pred[:, :, :, 0]
    y_pred_f = K.flatten(mu)
    intersection = K.sum(y_true_f * y_pred_f)
    smooth = 1.0
    return (2 * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def dice_loss(y_true, y_pred):
    return 1 - dice_coefficient(y_true, y_pred)


def recall_smooth(y_true, y_pred):
    y_pred_f = K.flatten(y_pred)
    y_true_f = K.flatten(y_true)
    intersection = K.sum(y_true_f * y_pred_f)
    return intersection / (K.sum(y_true_f) + K.epsilon())


def precision_smooth(y_true, y_pred):
    y_pred_f = K.flatten(y_pred)
    y_true_f = K.flatten(y_true)
    intersection = K.sum(y_true_f * y_pred_f)
    return intersection / (K.sum(y_pred_f) + K.epsilon())


def accuracy(y_true, y_pred):
    y_pred_f = K.flatten(y_pred)
    y_true_f = K.flatten(y_true)
    true_positives = K.sum(K.round(K.clip(y_true_f * y_pred_f, 0, 1)))
    true_negatives = K.sum(K.round(K.clip((1 - y_true_f) * (1 - y_pred_f), 0, 1)))
    total_pixels = K.cast(tf.size(y_true_f), K.floatx())
    return (true_positives + true_negatives) / total_pixels


CUSTOM_OBJECTS = {
    "dice_loss": dice_loss,
    "dice_coefficient": dice_coefficient,
    "precision_smooth": precision_smooth,
    "recall_smooth": recall_smooth,
    "accuracy": accuracy,
}


@lru_cache(maxsize=1)
def get_model():
    if not settings.model_path.exists():
        raise FileNotFoundError(f"Model file not found: {settings.model_path}")

    return tf.keras.models.load_model(
        settings.model_path,
        custom_objects=CUSTOM_OBJECTS,
        compile=False,
    )
