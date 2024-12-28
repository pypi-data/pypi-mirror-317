from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction, QActionGroup

class ThemeManager:
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"

    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = QSettings("YourCompany", "DocumentationEditor")

    def get_theme(self):
        return self.settings.value("theme", self.SYSTEM)

    def set_theme(self, theme):
        self.settings.setValue("theme", theme)
        self.apply_theme(theme)

    def apply_theme(self, theme):
        if theme == self.DARK:
            self._apply_dark_theme()
        elif theme == self.LIGHT:
            self._apply_light_theme()
        else:  # system
            self._apply_system_theme()

    def _apply_dark_theme(self):
        # Dark theme styles
        style = """
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #252526;
                color: #ffffff;
                border: 1px solid #3c3c3c;
            }
            QMenuBar {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #3c3c3c;
            }
            QMenu {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
            }
            QMenu::item:selected {
                background-color: #3c3c3c;
            }
        """
        self.main_window.setStyleSheet(style)
        self._update_preview_theme("dark")

    def _apply_light_theme(self):
        # Light theme styles
        style = """
            QMainWindow, QWidget {
                background-color: #ffffff;
                color: #000000;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #d0d0d0;
            }
            QMenuBar {
                background-color: #f0f0f0;
                color: #000000;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QMenu {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #d0d0d0;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
            }
        """
        self.main_window.setStyleSheet(style)
        self._update_preview_theme("light")

    def _apply_system_theme(self):
        self.main_window.setStyleSheet("")  # Reset to system theme
        self._update_preview_theme("default")

    def _update_preview_theme(self, theme):
        # Update the preview's mermaid theme
        self.main_window.current_preview_theme = theme
        self.main_window.update_preview()


