"""
Application menu bar.
"""

from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QMainWindow


class AppMenuBar:
    """Creates the application's menu bar."""

    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self._build()

        # Help menu
        self.user_guide_action = QAction("User Guide")
        self.keyboard_shortcuts_action = QAction("Keyboard Shortcuts")

        self.help_menu.addAction(self.user_guide_action)
        self.help_menu.addAction(self.keyboard_shortcuts_action)

        self.help_menu.addSeparator()

        self.about_action = QAction("About Universal Viewer")

        self.help_menu.addAction(self.about_action)

    def _build(self) -> None:
        menu_bar = self.window.menuBar()

        
        # Menus
        

        file_menu = menu_bar.addMenu("&File")
        edit_menu = menu_bar.addMenu("&Edit")
        view_menu = menu_bar.addMenu("&View")
        self.help_menu = menu_bar.addMenu("&Help")

        
        # File actions
        

        self.open_folder_action = QAction(
            "Open Folder...",
            self.window,
        )

        self.exit_action = QAction(
            "Exit",
            self.window,
        )

        
        # View actions
        

        self.refresh_action = QAction(
            "Refresh",
            self.window,
        )
        self.go_up_action = QAction(
            "Go Up",
            self.window,
        )


        
        # Edit actions
        

        self.cut_action = QAction(
            "Cut",
            self.window,
        )

        self.cut_action.setShortcut(
            "Ctrl+X"
        )

        self.copy_action = QAction(
            "Copy",
            self.window,
        )
        self.copy_action.setShortcut(
            "Ctrl+C"
        )

        self.copy_action.setShortcutContext(
            Qt.ApplicationShortcut
        )

        self.paste_action = QAction(
            "Paste",
            self.window,
        )
        self.paste_action.setShortcut(
            "Ctrl+V"
        )

        self.rename_action = QAction(
            "Rename",
            self.window,
        )

        self.rename_action.setShortcut("F2")


        self.delete_action = QAction(
            "Delete",
            self.window,
        )

        self.delete_action.setShortcut("Delete")


        self.select_all_action = QAction(
            "Select All",
            self.window,
        )

        self.select_all_action.setShortcut("Ctrl+A")

        
        # File menu
        

        file_menu.addAction(
            self.open_folder_action
        )

        file_menu.addSeparator()

        file_menu.addAction(
            self.exit_action
        )

        
        # View menu
        

        view_menu.addAction(
            self.refresh_action
        )

        view_menu.addAction(
            self.go_up_action
        )

        
        # Edit menu
        

        edit_menu.addAction(
            self.cut_action
        )

        edit_menu.addAction(
            self.copy_action
        )

        edit_menu.addAction(
            self.paste_action
        )

        edit_menu.addSeparator()

        edit_menu.addAction(
            self.rename_action
        )

        edit_menu.addAction(
            self.delete_action
        )

        edit_menu.addSeparator()

        edit_menu.addAction(
            self.select_all_action
        )