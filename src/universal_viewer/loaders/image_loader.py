"""
Universal image loader.
"""

from pathlib import Path

from PySide6.QtGui import QImage

from universal_viewer.loaders import (
    opencv_loader,
    pillow_loader,
    tiff_loader,
)
from universal_viewer.loaders.qimage_converter import (
    numpy_to_qimage,
)


class ImageLoader:
    @staticmethod
    def load(path: str | Path) -> QImage | None:
        path = Path(path)

        ext = path.suffix.lower()

        if ext in {".tif", ".tiff"}:
            image = tiff_loader.load(path)

        else:
            image = opencv_loader.load(path)

        if image is None:
            image = pillow_loader.load(path)

        if image is None:
            return None

        return numpy_to_qimage(image)
