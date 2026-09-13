"""
Main application window.
"""

from pathlib import Path

from PySide6.QtCore import (
    QMimeData,
    QProcess,
    QUrl,
    Qt,
    QTimer,
)

from PySide6.QtGui import (
    QClipboard,
)

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStackedWidget,
)

from universal_viewer.ui.menu_bar import AppMenuBar
from universal_viewer.ui.file_browser import FileBrowser
from universal_viewer.ui.image_viewer import ImageViewer
from universal_viewer.ui.pdf_viewer import PdfViewer
from universal_viewer.ui.status_bar import AppStatusBar
from universal_viewer.ui.tool_bar import AppToolBar


# Supported file types


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".webp",
    ".tif",
    ".tiff",
}

PDF_EXTENSIONS = {
    ".pdf",
}

DOCUMENT_EXTENSIONS = {
    ".docx",
    ".doc",
    ".odt",
    ".xlsx",
    ".xls",
    ".ods",
    ".pptx",
    ".ppt",
    ".odp",
}


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self._splitter: QSplitter | None = None

        # Setup

        self._setup_window()
        self._create_menu()
        self._create_toolbar()
        self._create_statusbar()
        self._create_central_widget()
        self._connect_actions()
        self._setup_keyboard_shortcuts()

        # Set splitter sizes after window is displayed.
        QTimer.singleShot(
            0,
            self._set_initial_splitter_sizes,
        )

    # Window

    def _setup_window(self) -> None:
        """Configure the main window."""

        self.setWindowTitle("Universal Viewer")

        self.setMinimumSize(
            1000,
            600,
        )

        screen = self.screen()

        if screen is None:
            self.resize(
                1400,
                800,
            )

            return

        geometry = screen.availableGeometry()

        width = int(geometry.width() * 0.90)

        height = int(geometry.height() * 0.90)

        self.resize(
            width,
            height,
        )

        x = geometry.x() + (geometry.width() - width) // 2

        y = geometry.y() + (geometry.height() - height) // 2

        self.move(
            x,
            y,
        )

    # Menu

    def _create_menu(self) -> None:
        """Create application menu."""

        self.menu = AppMenuBar(self)

    # Toolbar

    def _create_toolbar(self) -> None:
        """Create application toolbar."""

        self.toolbar = AppToolBar(self)

    # Status bar

    def _create_statusbar(self) -> None:
        """Create application status bar."""

        self.status = AppStatusBar()

        self.setStatusBar(self.status)

    # Central widget

    def _create_central_widget(self) -> None:
        """Create the main file-browser/viewer layout."""

        self._splitter = QSplitter(Qt.Horizontal)

        # File browser

        self.file_browser = FileBrowser()

        # Viewers

        self.image_viewer = ImageViewer()

        self.pdf_viewer = PdfViewer()

        # Viewer stack

        self.viewer_stack = QStackedWidget()

        self.viewer_stack.addWidget(self.image_viewer)

        self.viewer_stack.addWidget(self.pdf_viewer)

        # Splitter

        self._splitter.addWidget(self.file_browser)

        self._splitter.addWidget(self.viewer_stack)

        self._splitter.setChildrenCollapsible(False)

        self.file_browser.setMinimumWidth(400)

        self.viewer_stack.setMinimumWidth(400)

        self._splitter.setStretchFactor(
            0,
            1,
        )

        self._splitter.setStretchFactor(
            1,
            1,
        )

        self.setCentralWidget(self._splitter)

    # Splitter

    def _set_initial_splitter_sizes(
        self,
    ) -> None:
        """Set initial file-browser/viewer ratio."""

        if self._splitter is None:
            return

        total_width = self._splitter.width()

        left_width = int(total_width * 0.65)

        right_width = total_width - left_width

        self._splitter.setSizes(
            [
                left_width,
                right_width,
            ]
        )

    # Actions

    def _connect_actions(self) -> None:
        """Connect application actions."""

        # File menu

        self.menu.open_folder_action.triggered.connect(self._open_folder)

        self.menu.exit_action.triggered.connect(self.close)

        # Edit menu

        self.menu.copy_action.triggered.connect(self._copy)

        self.menu.cut_action.triggered.connect(self._cut)

        self.menu.paste_action.triggered.connect(self._paste)

        self.menu.rename_action.triggered.connect(self.file_browser.rename_selected)

        self.menu.delete_action.triggered.connect(self.file_browser.delete_selected)

        self.menu.select_all_action.triggered.connect(self.file_browser.select_all)

        # View menu

        self.menu.refresh_action.triggered.connect(self._refresh)

        self.menu.go_up_action.triggered.connect(self._go_up)

        # Toolbar

        self.toolbar.open_folder_action.triggered.connect(self._open_folder)

        self.toolbar.refresh_action.triggered.connect(self._refresh)

        self.toolbar.zoom_in_action.triggered.connect(self.image_viewer.zoom_in)

        self.toolbar.zoom_out_action.triggered.connect(self.image_viewer.zoom_out)

        self.toolbar.fit_action.triggered.connect(self.image_viewer.fit_image)

        # File browser

        self.file_browser.file_selected.connect(self._file_selected)

        self.menu.user_guide_action.triggered.connect(self.show_user_guide)
        self.menu.keyboard_shortcuts_action.triggered.connect(
            self.show_keyboard_shortcuts
        )
        self.menu.about_action.triggered.connect(self.show_about)

    # File selection

    def _file_selected(
        self,
        path: str,
    ) -> None:
        """Handle selected filesystem item."""

        self.status.showMessage(path)

        file_path = Path(path)

        # Ignore folders

        if not file_path.is_file():
            return

        suffix = file_path.suffix.lower()

        # Images

        if suffix in IMAGE_EXTENSIONS:
            self.viewer_stack.setCurrentWidget(self.image_viewer)

            self.image_viewer.load_image(file_path)

            return

        # PDF

        if suffix in PDF_EXTENSIONS:
            self.viewer_stack.setCurrentWidget(self.pdf_viewer)

            self.pdf_viewer.load_pdf(file_path)

            return

        # Documents

        if suffix in DOCUMENT_EXTENSIONS:
            # Clear old image.
            self.image_viewer.clear()

            # Do not leave the previous PDF visible.
            self.viewer_stack.setCurrentWidget(self.image_viewer)

            # Open with system application.
            self._open_external(file_path)

            return

        # Unsupported

        self.status.showMessage(f"Unsupported file type: {suffix}")

    # Open folder

    def _open_folder(self) -> None:
        """Open a folder and display it in the file browser."""

        folder = QFileDialog.getExistingDirectory(
            self,
            "Open Folder",
            str(Path.home()),
        )

        if not folder:
            return

        self.file_browser.set_root_path(folder)

        self.status.showMessage(folder)

    # Refresh

    def _refresh(self) -> None:
        """Refresh the file browser."""

        print(">>> MAIN WINDOW REFRESH <<<")

        self.file_browser.refresh()

        self.status.showMessage("File browser refreshed")

    # Go up

    def _go_up(self) -> None:
        """Navigate to the parent directory."""

        self.file_browser.go_up()

    # Copy

    def _copy(self) -> None:
        """Copy selected files or folders to the system clipboard."""

        print(">>> COPY ACTION FIRED <<<")

        paths = self.file_browser.selected_paths()

        print("Selected paths:", paths)

        if not paths:
            self.status.showMessage("Nothing selected")
            return

        valid_paths: list[Path] = []

        for path in paths:
            source = Path(path)

            if not source.exists():
                print("Skipping missing path:", source)
                continue

            valid_paths.append(source)

        if not valid_paths:
            self.status.showMessage("Selected items do not exist")
            return

        # Create MIME data

        mime_data = QMimeData()

        urls = [QUrl.fromLocalFile(str(path)) for path in valid_paths]

        # Standard file-manager format.
        mime_data.setUrls(urls)

        # GNOME/Nautilus format.
        gnome_lines = ["copy"]

        for url in urls:
            gnome_lines.append(url.toString(QUrl.FullyEncoded))

        gnome_data = "\n".join(gnome_lines) + "\n"

        mime_data.setData(
            "x-special/gnome-copied-files",
            gnome_data.encode("utf-8"),
        )

        # URI-list fallback.
        uri_data = "\r\n".join(url.toString(QUrl.FullyEncoded) for url in urls)

        mime_data.setData(
            "text/uri-list",
            (uri_data + "\r\n").encode("utf-8"),
        )

        # Put into system clipboard

        clipboard = QApplication.clipboard()

        clipboard.setMimeData(
            mime_data,
            QClipboard.Clipboard,
        )

        # Debug

        current = clipboard.mimeData()

        print("Clipboard formats:", current.formats())
        print("Clipboard URLs:", current.urls())

        if current.hasFormat("x-special/gnome-copied-files"):
            print(
                "GNOME data:",
                bytes(current.data("x-special/gnome-copied-files")).decode(
                    "utf-8",
                    errors="replace",
                ),
            )

        self.status.showMessage(f"Copied {len(valid_paths)} item(s)")

    # Paste

    def _paste(self) -> None:
        """Paste files from the system clipboard."""

        print(">>> MAIN WINDOW PASTE FIRED <<<")

        self.file_browser.paste_files()

        self.status.showMessage("Paste completed")

    # External application

    def _open_external(
        self,
        path: Path,
    ) -> None:
        """Open a file using the system default application."""

        QProcess.startDetached(
            "xdg-open",
            [str(path)],
        )

    # Keyboard shortcuts

    def _setup_keyboard_shortcuts(self) -> None:
        """Configure application keyboard shortcuts."""

        # Cut

        self.menu.cut_action.setShortcut("Ctrl+X")
        self.menu.cut_action.setShortcutContext(Qt.ApplicationShortcut)

        # Copy

        self.menu.copy_action.setShortcut("Ctrl+C")
        self.menu.copy_action.setShortcutContext(Qt.ApplicationShortcut)

        # Paste

        self.menu.paste_action.setShortcut("Ctrl+V")
        self.menu.paste_action.setShortcutContext(Qt.ApplicationShortcut)

        # Rename

        self.menu.rename_action.setShortcut("F2")
        self.menu.rename_action.setShortcutContext(Qt.WindowShortcut)

        # Delete

        self.menu.delete_action.setShortcut("Delete")
        self.menu.delete_action.setShortcutContext(Qt.WindowShortcut)

        # Select All

        self.menu.select_all_action.setShortcut("Ctrl+A")
        self.menu.select_all_action.setShortcutContext(Qt.WindowShortcut)

    # Cut

    def _cut(self) -> None:
        """Cut selected files or folders to the system clipboard."""

        print(">>> CUT ACTION FIRED <<<")

        paths = self.file_browser.selected_paths()

        print(
            "Selected paths:",
            paths,
        )

        if not paths:
            self.status.showMessage("Nothing selected")

            return

        valid_paths: list[Path] = []

        for path in paths:
            source = Path(path)

            if not source.exists():
                print(
                    "Skipping missing path:",
                    source,
                )

                continue

            valid_paths.append(source)

        if not valid_paths:
            self.status.showMessage("Selected items do not exist")

            return

        # Create MIME data

        mime_data = QMimeData()

        urls = [QUrl.fromLocalFile(str(path)) for path in valid_paths]

        # Standard Linux file-manager format.
        mime_data.setUrls(urls)

        gnome_lines = ["cut"]

        for path in valid_paths:
            url = QUrl.fromLocalFile(str(path))

            gnome_lines.append(url.toString(QUrl.FullyEncoded))

        gnome_data = "\n".join(gnome_lines) + "\n"

        mime_data.setData(
            "x-special/gnome-copied-files",
            gnome_data.encode("utf-8"),
        )

        # URI-list fallback.
        uri_data = "\r\n".join(url.toString(QUrl.FullyEncoded) for url in urls)

        mime_data.setData(
            "text/uri-list",
            (uri_data + "\r\n").encode("utf-8"),
        )

        # Put into system clipboard

        clipboard = QApplication.clipboard()

        clipboard.setMimeData(
            mime_data,
            QClipboard.Clipboard,
        )

        print("CUT clipboard created.")

        print(
            "Clipboard formats:",
            clipboard.mimeData().formats(),
        )

        print(
            "Clipboard URLs:",
            clipboard.mimeData().urls(),
        )

        self.status.showMessage(f"Cut {len(valid_paths)} item(s)")

    def show_user_guide(self):
        QMessageBox.information(
            self,
            "User Guide",
            "Universal Viewer\n\n"
            "• Open Folder - Open a folder to browse files.\n"
            "• Refresh - Refresh the current folder.\n"
            "• Go Up - Move to the parent folder.\n"
            "• Zoom + - Zoom in on the image.\n"
            "• Zoom - - Zoom out on the image.\n"
            "• Fit - Fit the image to the viewer.\n"
            "• Copy - Copy the selected file.\n"
            "• Cut - Cut the selected file.\n"
            "• Paste - Paste the copied or cut file.\n"
            "• Rename - Rename the selected file.\n"
            "• Delete - Delete the selected file.",
        )

    def show_keyboard_shortcuts(self):
        QMessageBox.information(
            self,
            "Keyboard Shortcuts",
            "Keyboard Shortcuts\n\n"
            "Ctrl + C    Copy\n"
            "Ctrl + X    Cut\n"
            "Ctrl + V    Paste\n"
            "F2          Rename\n"
            "Delete      Delete\n"
            "Ctrl + R    Refresh\n"
            "Enter       Open\n"
            "Backspace   Go Up",
        )

    def show_about(self):
        QMessageBox.about(
            self,
            "About Universal Viewer",
            "<h3>Universal Viewer</h3>"
            "<p>A simple file manager and document viewer.</p>"
            "<p>Version 0.1.0</p>"
            "<p>Built with Python and PySide6.</p>",
        )
