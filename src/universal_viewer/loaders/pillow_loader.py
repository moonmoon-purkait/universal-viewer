"""
Pillow fallback loader.
"""

from pathlib import Path

import numpy as np
from PIL import Image


def load(path: str | Path):
    try:
        image = Image.open(path)

        return np.array(image)

    except Exception:
        return None
