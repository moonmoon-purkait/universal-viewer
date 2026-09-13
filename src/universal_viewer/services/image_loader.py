"""
Image loading service.
"""

from pathlib import Path

import cv2
from PySide6.QtGui import QImage


class ImageLoader:
    """Loads images from disk."""

    @staticmethod
    def load(path: str | Path) -> QImage | None:
        path = str(path)

        image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

        if image is None:
            return None

        # grayscale
        if len(image.shape) == 2:

            h, w = image.shape

            bytes_per_line = w

            return QImage(
                image.data,
                w,
                h,
                bytes_per_line,
                QImage.Format_Grayscale8,
            ).copy()

        # color
        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

        h, w, ch = image.shape

        bytes_per_line = ch * w

        return QImage(
            image.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888,
        ).copy()