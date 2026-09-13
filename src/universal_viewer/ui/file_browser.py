"""
File browser widget.
"""

from pathlib import Path
import shutil

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QFileSystemModel,
    QHeaderView,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QInputDialog,
)


class FileBrowser(QWidget):
    """
    File browser widget.

    Displays the local filesystem and emits the
    selected file path.
    """

    file_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self._model = QFileSystemModel(self)
        self._tree = QTreeView(self)

        self._setup_model()
        self._setup_tree()
        self._create_layout()
        self._connect_signals()


    # Model


    def _setup_model(self) -> None:
        """Configure the filesystem model."""

        root = str(Path.home())

        # Allow filesystem modifications such as rename/delete.
        self._model.setReadOnly(False)

        self._model.setRootPath(root)


    # Tree


    def _setup_tree(self) -> None:
        """Configure the file tree."""

        root = str(Path.home())

        self._tree.setModel(self._model)

        self._tree.setRootIndex(
            self._model.index(root)
        )

        
        # General appearance
        

        self._tree.setAnimated(True)

        self._tree.setIndentation(20)

        self._tree.setSortingEnabled(True)

        self._tree.setAlternatingRowColors(True)

        self._tree.setUniformRowHeights(True)

        self._tree.setWordWrap(False)

        
        # Selection
        

        self._tree.setSelectionMode(
            QTreeView.ExtendedSelection
        )

        self._tree.setSelectionBehavior(
            QTreeView.SelectRows
        )

        
        # Header
        

        header = self._tree.header()

        header.setStretchLastSection(False)

        # Name
        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch,
        )

        # Size
        header.setSectionResizeMode(
            1,
            QHeaderView.Fixed,
        )

        # Type
        header.setSectionResizeMode(
            2,
            QHeaderView.Fixed,
        )

        # Date Modified
        header.setSectionResizeMode(
            3,
            QHeaderView.Fixed,
        )

        
        # Column widths
        

        header.resizeSection(
            1,
            110,
        )

        header.resizeSection(
            2,
            170,
        )

        header.resizeSection(
            3,
            180,
        )

        
        # Header appearance
        

        header.setDefaultAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )

        header.setMinimumSectionSize(60)


    # Layout


    def _create_layout(self) -> None:
        """Create widget layout."""

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self._tree.setMinimumWidth(500)

        layout.addWidget(
            self._tree
        )


    # Signals


    def _connect_signals(self) -> None:
        """Connect tree signals."""

        self._tree.clicked.connect(
            self._on_item_clicked
        )

        self._tree.selectionModel().currentChanged.connect(
            self._on_current_changed
        )

    def _on_current_changed(
        self,
        current,
        previous,
    ) -> None:
        """Handle keyboard or programmatic selection changes."""

        if not current.isValid():
            return

        path = self._model.filePath(
            current
        )

        self.file_selected.emit(
            path
        )


    # Selection


    def _on_item_clicked(
        self,
        index,
    ) -> None:
        """Handle selected filesystem item."""

        path = self._model.filePath(
            index
        )

        self.file_selected.emit(
            path
        )


    # Public API


    def set_root_path(
        self,
        path: str,
    ) -> None:
        """Change the displayed root directory."""

        path = str(
            Path(path).expanduser().resolve()
        )

        self._model.setRootPath(
            path
        )

        self._tree.setRootIndex(
            self._model.index(path)
        )

    def refresh(self) -> None:
        """Refresh the currently displayed directory."""

        root_index = self._tree.rootIndex()

        if not root_index.isValid():
            print("Refresh: invalid root index")
            return

        path = self._model.filePath(root_index)

        print("Refresh path:", path)

        if not path:
            print("Refresh: empty path")
            return

        # Force QFileSystemModel to re-read the directory.
        self._model.setRootPath("")
        self._model.setRootPath(path)

        self._tree.setRootIndex(
            self._model.index(path)
        )

        print("Refresh completed:", path)

    def go_up(self) -> None:
        """Navigate to the parent directory."""

        root_index = self._tree.rootIndex()

        if not root_index.isValid():
            return

        current_path = Path(
            self._model.filePath(
                root_index
            )
        )

        if not current_path.is_dir():
            return

        parent_path = current_path.parent

        # Already at filesystem root.
        if parent_path == current_path:
            return

        self.set_root_path(
            str(parent_path)
        )


    # Selection API


    def selected_path(self) -> str | None:
        """Return the currently selected filesystem path."""

        index = self._tree.currentIndex()

        if not index.isValid():
            return None

        return self._model.filePath(
            index
        )


    # Paste


    def paste_files(self) -> None:
        """
        Paste files from the system clipboard.

        Supports:

        - Copy
        - Cut

        Clipboard formats:

        - text/uri-list
        - x-special/gnome-copied-files
        """

        print(
            ">>> PASTE ACTION FIRED <<<"
        )

        clipboard = QApplication.clipboard()

        mime_data = clipboard.mimeData()

        if mime_data is None:
            print(
                "Clipboard MIME data is empty."
            )
            return

        print(
            "Clipboard formats:",
            mime_data.formats(),
        )

        
        # Determine operation
        

        operation = "copy"

        if mime_data.hasFormat(
            "x-special/gnome-copied-files"
        ):
            try:
                gnome_data = bytes(
                    mime_data.data(
                        "x-special/gnome-copied-files"
                    )
                ).decode(
                    "utf-8",
                    errors="replace",
                )

                lines = [
                    line.strip()
                    for line in gnome_data.splitlines()
                    if line.strip()
                ]

                if lines:
                    operation = lines[0].lower()

            except Exception as exc:
                print(
                    "Could not read clipboard operation:",
                    exc,
                )

        print(
            "Clipboard operation:",
            operation,
        )

        if operation not in {
            "copy",
            "cut",
        }:
            operation = "copy"

        
        # Get clipboard URLs
        

        urls = []

        if mime_data.hasUrls():
            urls = mime_data.urls()

        if not urls:
            print(
                "Clipboard does not contain files."
            )
            return

        
        # Determine destination
        

        destination = self._paste_destination()

        if destination is None:
            print(
                "Could not determine paste destination."
            )
            return

        print(
            "Paste destination:",
            destination,
        )

        
        # Process files
        

        processed_count = 0

        for url in urls:

            if not url.isLocalFile():

                print(
                    "Skipping non-local URL:",
                    url,
                )

                continue

            source = Path(
                url.toLocalFile()
            )

            print(
                "Clipboard source:",
                source,
            )

            if not source.exists():

                print(
                    "Source does not exist:",
                    source,
                )

                continue

            target = (
                destination
                / source.name
            )

            
            # Prevent moving a directory into itself.
            

            try:

                source_resolved = (
                    source.resolve()
                )

                destination_resolved = (
                    destination.resolve()
                )

                if source.is_dir():

                    if (
                        destination_resolved
                        == source_resolved
                        or destination_resolved.is_relative_to(
                            source_resolved
                        )
                    ):

                        print(
                            "Cannot paste a folder inside itself:",
                            source,
                        )

                        continue

            except OSError:

                pass

            
            # Cut into the same directory
            

            if operation == "cut":

                try:

                    if (
                        source.resolve()
                        == target.resolve()
                    ):

                        print(
                            "Cut source and target are identical."
                        )

                        processed_count += 1

                        continue

                except OSError:

                    pass

            
            # Avoid overwriting existing items.
            

            target = self._unique_target(
                target
            )

            
            # COPY
            

            if operation == "copy":

                try:

                    if source.is_dir():

                        shutil.copytree(
                            source,
                            target,
                        )

                    else:

                        shutil.copy2(
                            source,
                            target,
                        )

                    print(
                        "COPY SUCCESS:"
                    )

                    print(
                        f"  From: {source}"
                    )

                    print(
                        f"  To:   {target}"
                    )

                    processed_count += 1

                except Exception as exc:

                    print(
                        "COPY FAILED:"
                    )

                    print(
                        f"  From: {source}"
                    )

                    print(
                        f"  To:   {target}"
                    )

                    print(
                        f"  Error: {exc}"
                    )

            
            # CUT / MOVE
            

            elif operation == "cut":

                try:

                    shutil.move(
                        source,
                        target,
                    )

                    print(
                        "MOVE SUCCESS:"
                    )

                    print(
                        f"  From: {source}"
                    )

                    print(
                        f"  To:   {target}"
                    )

                    processed_count += 1

                except Exception as exc:

                    print(
                        "MOVE FAILED:"
                    )

                    print(
                        f"  From: {source}"
                    )

                    print(
                        f"  To:   {target}"
                    )

                    print(
                        f"  Error: {exc}"
                    )

        
        # Refresh browser
        

        if processed_count > 0:

            self.refresh()

            print(
                f"{operation.capitalize()} processed "
                f"{processed_count} item(s)."
            )

        else:

            print(
                "Nothing was pasted."
            )


    # Paste destination


    def _paste_destination(
        self,
    ) -> Path | None:
        """
        Determine where pasted files should go.

        If a folder is selected:
            paste inside the folder.

        If a file is selected:
            paste beside the file.

        If nothing is selected:
            paste into current root directory.
        """

        current_index = (
            self._tree.currentIndex()
        )

        
        # Selected item
        

        if current_index.isValid():

            selected_path = Path(
                self._model.filePath(
                    current_index
                )
            )

            if selected_path.is_dir():

                return selected_path

            if selected_path.is_file():

                return selected_path.parent

        
        # No selected item
        

        root_index = (
            self._tree.rootIndex()
        )

        if not root_index.isValid():

            return None

        root_path = Path(
            self._model.filePath(
                root_index
            )
        )

        if root_path.is_dir():

            return root_path

        return None


    # Unique target


    def _unique_target(
        self,
        target: Path,
    ) -> Path:
        """
        Create a unique destination path.

        Example:

            image.jpg
            image (1).jpg
            image (2).jpg
        """

        if not target.exists():

            return target

        parent = target.parent

        stem = target.stem

        suffix = target.suffix

        counter = 1

        while True:

            candidate = (
                parent
                / f"{stem} ({counter}){suffix}"
            )

            if not candidate.exists():

                return candidate

            counter += 1


    # Rename


    def rename_selected(self) -> None:
        """Rename the currently selected file or folder."""

        index = self._tree.currentIndex()

        if not index.isValid():
            return

        # Always use the Name column.
        # currentIndex() may point to Size, Type, or Date Modified.
        index = index.siblingAtColumn(0)

        old_path = Path(
            self._model.filePath(index)
        )

        old_name = old_path.name

        if not old_path.exists():
            QMessageBox.warning(
                self,
                "Rename Failed",
                f"File or folder does not exist:\n{old_path}",
            )
            return

        new_name, accepted = QInputDialog.getText(
            self,
            "Rename",
            "New name:",
            text=old_name,
        )

        if not accepted:
            return

        new_name = new_name.strip()

        if not new_name:
            return

        if new_name == old_name:
            return

        # Prevent invalid path names.
        if "/" in new_name or "\\" in new_name:
            QMessageBox.warning(
                self,
                "Rename Failed",
                "The new name cannot contain '/' or '\\'.",
            )
            return

        new_path = old_path.parent / new_name

        # Don't overwrite an existing file/folder.
        if new_path.exists():
            QMessageBox.warning(
                self,
                "Rename Failed",
                f"An item with this name already exists:\n\n"
                f"{new_name}",
            )
            return

        # Let QFileSystemModel perform the rename.
        success = self._model.setData(
            index,
            new_name,
            Qt.ItemDataRole.EditRole,
        )

        if not success:
            QMessageBox.warning(
                self,
                "Rename Failed",
                f"Could not rename:\n{old_name}",
            )
            return

        self.status_message = (
            f"Renamed: {old_name} → {new_name}"
        )

    # Delete


    def delete_selected(self) -> None:
        """Delete the currently selected file or folder."""

        index = self._tree.currentIndex()

        if not index.isValid():
            return

        path = Path(
            self._model.filePath(index)
        )

        answer = QMessageBox.question(
            self,
            "Delete",
            f"Are you sure you want to delete:\n\n{path.name}?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        success = self._model.remove(index)

        if not success:
            QMessageBox.warning(
                self,
                "Delete Failed",
                f"Could not delete:\n{path}",
            )


    # Select All


    def select_all(self) -> None:
        """Select all visible files and folders."""

        self._tree.selectAll()

    def selected_paths(self) -> list[str]:
        """Return all selected filesystem paths."""

        indexes = self._tree.selectionModel().selectedRows(
            0
        )

        paths: list[str] = []

        for index in indexes:
            path = self._model.filePath(index)

            if path:
                paths.append(path)

        return paths