"""
OpenCV image loader.
"""

from pathlib import Path

import cv2
import numpy as np


def load(path: str | Path) -> np.ndarray | None:
    image = cv2.imread(
        str(path),
        cv2.IMREAD_UNCHANGED,
    )

    return image
