"""
Image Viewer Widget.
"""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
)
from universal_viewer.loaders.image_loader import ImageLoader

class ImageViewer(QGraphicsView):
    """ Graphics view for displaying and interacting with images. 
    
    Supports loading images, zooming, panning, and fitting images to 
    the available viewing area. 
    """

    def __init__(self) -> None:
        """Initialize the image viewer and configure its graphics scene."""
        super().__init__()

        self._scene = QGraphicsScene(self)

        self._pixmap_item = QGraphicsPixmapItem()

        self._scene.addItem(self._pixmap_item)

        self.setScene(self._scene)

        self._setup()

    def _setup(self) -> None:
        """Configure rendering, panning, and transformation behavior."""
        self.setRenderHints(
            self.renderHints()
        )

        self.setDragMode(
            QGraphicsView.ScrollHandDrag
        )

        self.setTransformationAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.AnchorUnderMouse
        )
    

    def load_image(
        self,
        path: str | Path,
    ) -> None:
        """Load an image from the given path and display it in the viewer."""

        image = ImageLoader.load(path)

        if image is None:

            self._pixmap_item.setPixmap(QPixmap())

            return

        pixmap = QPixmap.fromImage(image)

        self._pixmap_item.setPixmap(pixmap)

        self.setSceneRect(
            self._pixmap_item.boundingRect()
        )

        self.fitInView(
            self._pixmap_item,
            Qt.KeepAspectRatio,
        )
    
    def zoom_in(self) -> None:
        """Increase the current image zoom level."""
        factor = 1.20

        self.scale(
            factor,
            factor,
        )

    def zoom_out(self) -> None:
        """Decrease the current image zoom level."""
        factor = 1.20

        self.scale(
            1 / factor,
            1 / factor,
        )

    def fit_image(self) -> None:
        """Fit the image inside the viewer."""

        if self._pixmap_item.pixmap().isNull():
            return

        self.fitInView(
            self._pixmap_item,
            Qt.KeepAspectRatio,
        )

    def wheelEvent(self, event):
        """Zoom the view in or out using the mouse wheel."""
        factor = 1.20

        if event.angleDelta().y() > 0:

            self.scale(
                factor,
                factor,
            )

        else:

            self.scale(
                1 / factor,
                1 / factor,
            )

    def clear(self) -> None:
        """Clear the current image."""

        self._pixmap_item.setPixmap(QPixmap())

        self._scene.clear()

        self._pixmap_item = QGraphicsPixmapItem()

        self._scene.addItem(
            self._pixmap_item
        )