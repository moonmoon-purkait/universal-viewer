"""
Application status bar.
"""

from PySide6.QtWidgets import QStatusBar


class AppStatusBar(QStatusBar):
    """Status bar."""

    def __init__(self) -> None:
        super().__init__()

        self.showMessage("Ready")
