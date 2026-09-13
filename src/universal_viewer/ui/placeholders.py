"""
Temporary placeholder widgets.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class FileBrowserPlaceholder(QLabel):
    def __init__(self) -> None:
        super().__init__("File Browser")

        self.setAlignment(Qt.AlignCenter)


class ViewerPlaceholder(QLabel):
    def __init__(self) -> None:
        super().__init__("Image Viewer")

        self.setAlignment(Qt.AlignCenter)
