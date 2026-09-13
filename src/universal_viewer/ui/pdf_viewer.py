"""
PDF viewer widget.
"""

from pathlib import Path

from PySide6.QtCore import QPointF, Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class PdfViewer(QPdfView):
    """Viewer for PDF documents."""

    def __init__(self) -> None:
        super().__init__()

        self._document = QPdfDocument(self)

        self.setDocument(self._document)

    # Public API

    def load_pdf(
        self,
        path: str | Path,
    ) -> None:
        """Load a PDF document."""

        path = Path(path)

        if not path.is_file():
            return

        self._document.load(str(path))

    def clear(self) -> None:
        """Clear the current PDF."""

        self._document.close()

    # Page navigation

    def next_page(self) -> None:
        """Show the next PDF page."""

        page = self.pageNavigator().currentPage()

        if page < self._document.pageCount() - 1:
            self.pageNavigator().jump(
                page + 1,
                QPointF(0, 0),
            )

    def previous_page(self) -> None:
        """Show the previous PDF page."""

        page = self.pageNavigator().currentPage()

        if page > 0:
            self.pageNavigator().jump(
                page - 1,
                QPointF(0, 0),
            )

    # Keyboard

    def keyPressEvent(self, event) -> None:
        """Handle PDF page navigation."""

        if event.key() == Qt.Key_Right:
            self.next_page()
            return

        if event.key() == Qt.Key_Left:
            self.previous_page()
            return

        super().keyPressEvent(event)
