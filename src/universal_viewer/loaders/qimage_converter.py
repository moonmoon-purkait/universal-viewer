"""
Convert numpy arrays to QImage.
"""

from __future__ import annotations

import cv2
import numpy as np
from PySide6.QtGui import QImage


def numpy_to_qimage(image: np.ndarray) -> QImage:
    """
    Convert a NumPy image to QImage.
    """

    if image.ndim == 2:
        h, w = image.shape

        return QImage(
            image.data,
            w,
            h,
            w,
            QImage.Format_Grayscale8,
        ).copy()

    if image.shape[2] == 3:
        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

        h, w, c = image.shape

        return QImage(
            image.data,
            w,
            h,
            c * w,
            QImage.Format_RGB888,
        ).copy()

    if image.shape[2] == 4:
        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGRA2RGBA,
        )

        h, w, c = image.shape

        return QImage(
            image.data,
            w,
            h,
            c * w,
            QImage.Format_RGBA8888,
        ).copy()

    raise ValueError("Unsupported image format")
