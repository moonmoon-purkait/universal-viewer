"""
Application toolbar.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QToolBar


class AppToolBar(QToolBar):
    """Main toolbar."""

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__("Main Toolbar", parent)

        self.setMovable(False)

        parent.addToolBar(
            Qt.TopToolBarArea,
            self,
        )

        
        # Actions
        

        self.open_folder_action = QAction(
            "Open Folder",
            self,
        )

        self.refresh_action = QAction(
            "Refresh",
            self,
        )

        self.zoom_in_action = QAction(
            "Zoom +",
            self,
        )

        self.zoom_out_action = QAction(
            "Zoom -",
            self,
        )

        self.fit_action = QAction(
            "Fit",
            self,
        )

        
        # Toolbar
        

        self.addAction(
            self.open_folder_action
        )

        self.addSeparator()

        self.addAction(
            self.refresh_action
        )

        self.addSeparator()

        self.addAction(
            self.zoom_in_action
        )

        self.addAction(
            self.zoom_out_action
        )

        self.addSeparator()

        self.addAction(
            self.fit_action
        )