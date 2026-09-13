"""
TIFF loader.
"""

from pathlib import Path

import numpy as np
import tifffile


def load(path: str | Path) -> np.ndarray | None:

    try:
        image = tifffile.imread(path)

        return image

    except Exception:

        return None