"""
Application startup.

Creates QApplication and launches the main window.
"""

import sys
from PySide6.QtWidgets import QApplication
from universal_viewer.ui.main_window import MainWindow


def run() -> None:
    """Create and execute the Qt application."""

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
