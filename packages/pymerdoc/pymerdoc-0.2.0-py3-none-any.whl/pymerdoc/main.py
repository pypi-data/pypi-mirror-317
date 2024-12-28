import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QSplitter, QTextEdit, QMenuBar, QMenu, QMessageBox, QFileDialog)
from PyQt6.QtGui import QAction, QKeySequence, QActionGroup
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QTimer
import markdown
import re

from pymerdoc.mc import MermaidConverterDialog
from pymerdoc.gm import GifMakerDialog
from pymerdoc.theme_manager import ThemeManager

# def create_settings_menu(window):
    # Add Settings menu to menubar
        # Create settings menu
    # create_settings_menu(window)
    # return settings_menu

class MarkdownMermaidEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Documentation Editor")
        self.theme_manager = ThemeManager(self)

        screen = QApplication.primaryScreen().geometry()
        width = int(screen.width() * 0.5)
        height = int(screen.height() * 0.5)
        # Calculate center position
        left = int((screen.width() - width) / 2)
        top = int((screen.height() - height) / 2)
        # Set window geometry
        self.setGeometry(left, top, width, height)
        # Create menu bar
        self.create_menu_bar()

        # Initialize GIF maker
        self.gif_maker = None

        # Create the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create a splitter for resizable panes
        splitter = QSplitter()
        layout.addWidget(splitter)

        # Left pane: Editor
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)

        # Editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Enter your Markdown content here...\nUse ```mermaid blocks for diagrams")
        editor_layout.addWidget(self.editor)

        # Right pane: Preview
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)

        # Web view for preview
        self.web_view = QWebEngineView()
        preview_layout.addWidget(self.web_view)

        # Add both panes to splitter
        splitter.addWidget(editor_widget)
        splitter.addWidget(preview_widget)
        splitter.setSizes([400, 800])

        # Set up preview timer for debouncing
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.update_preview)

        # Connect signals
        self.editor.textChanged.connect(self.start_preview_timer)

        # Initialize current file path
        self.current_file = None
        # Initialize theme manager
        self.current_preview_theme = "default"  # For mermaid theme tracking



        # Apply saved theme
        self.theme_manager.apply_theme(self.theme_manager.get_theme())

    def start_preview_timer(self):
        """Start timer for delayed preview update"""
        self.preview_timer.start(1000)  # 1 second delay

    def _process_mermaid_blocks(self, content):
        """Convert markdown code blocks to HTML with special handling for mermaid"""
        # Pattern to match mermaid code blocks
        pattern = r'```mermaid\n(.*?)\n```'

        def replace_mermaid(match):
            diagram_content = match.group(1)
            return f'<div class="mermaid">\n{diagram_content}\n</div>'

        # Replace mermaid blocks before markdown conversion
        processed_content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)
        return processed_content

    def _convert_markdown_to_html(self, content):
        """Convert markdown to HTML while preserving mermaid diagrams"""
        # First process mermaid blocks
        processed_content = self._process_mermaid_blocks(content)

        # Convert to HTML using the markdown library
        md = markdown.Markdown(extensions=['fenced_code', 'tables', 'codehilite'])
        html_content = md.convert(processed_content)

        return html_content

    def create_menu_bar(self):
        """Create and initialize all menus"""
        menubar = self.menuBar()

        # Create all menus
        self._create_file_menu(menubar)
        self._create_tools_menu(menubar)
        self._create_settings_menu(menubar)
        self._create_help_menu(menubar)

    def create_mermaid_converter_menu(self, menubar):
        mermaid_converter_action = QAction("Mermaid Converter", self)
        mermaid_converter_action.triggered.connect(self.show_mermaid_converter)
        menubar.addAction(mermaid_converter_action)
    def _create_file_menu(self, menubar):
        """Create File menu and its actions"""
        file_menu = menubar.addMenu("File")

        # Define file actions
        actions = [
            ("New", QKeySequence.StandardKey.New, self.new_file),
            ("Open", QKeySequence.StandardKey.Open, self.open_file),
            ("Save", QKeySequence.StandardKey.Save, self.save_file),
            ("Save As...", QKeySequence.StandardKey.SaveAs, self.save_file_as),
            (None, None, None),  # Separator
            ("Exit", QKeySequence.StandardKey.Quit, self.close)
        ]

        # Create and add actions
        for name, shortcut, handler in actions:
            if name is None:  # Add separator
                file_menu.addSeparator()
                continue

            action = QAction(name, self)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(handler)
            file_menu.addAction(action)

    def _create_tools_menu(self, menubar):
        """Create Tools menu and its actions"""
        tools_menu = menubar.addMenu("Tools")

        # Add GIF Maker action
        gif_maker_action = QAction("GIF Maker", self)
        gif_maker_action.triggered.connect(self.show_gif_maker)
        tools_menu.addAction(gif_maker_action)
        self.create_mermaid_converter_menu(tools_menu)

    def _create_settings_menu(self, menubar):
        """Create Settings menu with theme options"""
        settings_menu = menubar.addMenu("Settings")

        # Create Theme submenu
        theme_menu = QMenu("Theme", self)
        settings_menu.addMenu(theme_menu)

        # Create theme action group
        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)

        # Define themes
        themes = [
            ("System", ThemeManager.SYSTEM),
            ("Light", ThemeManager.LIGHT),
            ("Dark", ThemeManager.DARK)
        ]

        # Create theme actions
        for theme_name, theme_value in themes:
            action = QAction(theme_name, self, checkable=True)
            action.setData(theme_value)
            theme_group.addAction(action)
            theme_menu.addAction(action)
            if theme_value == self.theme_manager.get_theme():
                action.setChecked(True)

        # Connect theme actions
        theme_group.triggered.connect(
            lambda action: self.theme_manager.set_theme(action.data())
        )

    def _create_help_menu(self, menubar):
        """Create Help menu and its actions"""
        help_menu = menubar.addMenu("Help")

        # Add About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def new_file(self):
        """Create a new file"""
        if self.maybe_save():
            self.editor.clear()
            self.current_file = None
            self.setWindowTitle("Documentation Editor - Untitled")

    def show_mermaid_converter(self):
        """Show the Mermaid converter dialog"""
        try:
            dialog = MermaidConverterDialog(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.warning(self, "Error",
                                f"Could not open Mermaid Converter: {str(e)}")
    def open_file(self):
        """Open a markdown file"""
        if self.maybe_save():
            filename, _ = QFileDialog.getOpenFileName(
                self, "Open Markdown File", "",
                "Markdown Files (*.md);;All Files (*)"
            )
            if filename:
                try:
                    with open(filename, 'r', encoding='utf-8') as file:
                        self.editor.setPlainText(file.read())
                    self.current_file = filename
                    self.setWindowTitle(f"Documentation Editor - {filename}")
                except Exception as e:
                    QMessageBox.warning(self, "Error",
                                        f"Could not open file: {str(e)}")

    def save_file(self):
        """Save the current file"""
        if self.current_file:
            self._save_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        """Save the current file with a new name"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Markdown File", "",
            "Markdown Files (*.md);;All Files (*)"
        )
        if filename:
            self._save_file(filename)

    def _save_file(self, filename):
        """Save the file to disk"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.editor.toPlainText())
            self.current_file = filename
            self.setWindowTitle(f"Documentation Editor - {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Error",
                                f"Could not save file: {str(e)}")

    def maybe_save(self):
        """Check if we need to save modifications"""
        if not self.editor.document().isModified():
            return True

        ret = QMessageBox.warning(
            self, "Application",
            "The document has been modified.\nDo you want to save your changes?",
            QMessageBox.StandardButton.Save |
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )

        if ret == QMessageBox.StandardButton.Save:
            self.save_file()
            return True
        elif ret == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def show_gif_maker(self):
        """Show the GIF maker dialog"""
        dialog = GifMakerDialog(self)
        dialog.exec()

    # def show_gif_maker(self):
    #     """Show the GIF maker dialog"""
    #     try:
    #         from gif_maker import GifMakerDialog
    #         dialog = GifMakerDialog(self)
    #         dialog.exec()
    #     except Exception as e:
    #         QMessageBox.warning(self, "Error",
    #                             f"Could not open GIF Maker: {str(e)}")

    def show_about_dialog(self):
        """Show the About dialog"""
        about_text = """
        <h3>PyMerDoc - Python Markdown Editor</h3>
        <p>A modern, feature-rich documentation editor built with PyQt6.</p>
        <p><b>Features:</b></p>
        <ul>
            <li>Real-time Markdown preview with syntax highlighting</li>
            <li>Mermaid diagram integration with live preview and export</li>
            <li>PNG to GIF converter with customizable settings</li>
            <li>Theme support (Light/Dark/System)</li>
            <li>Full file management capabilities</li>
        </ul>
        <p><b>Tools:</b></p>
        <ul>
            <li>Mermaid Diagram Converter - Create, preview, and export diagrams</li>
            <li>GIF Maker - Convert PNG sequences to animated GIFs</li>
        </ul>
        <p>Version 0.1.0</p>
        <p>Source code: <a href="https://github.com/scottpeterman/pymerdoc">github.com/scottpeterman/pymerdoc</a></p>
        <p>© 2024 Scott Peterman</p>
        """
        QMessageBox.about(self, "About PyMerDoc", about_text)


    def closeEvent(self, event):
        """Handle application closing"""
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    def update_preview(self):
        """Update the preview with current content"""
        content = self.editor.toPlainText()

        # Convert markdown to HTML
        html_content = self._convert_markdown_to_html(content)

        # Determine preview theme
        preview_bg = "#ffffff" if self.current_preview_theme == "light" else "#1e1e1e"
        preview_color = "#24292e" if self.current_preview_theme == "light" else "#ffffff"

        # Create complete HTML document
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ 
                    margin: 0; 
                    padding: 20px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: {preview_color};
                    background-color: {preview_bg};
                }}
                pre {{ 
                    background-color: {'#f6f8fa' if self.current_preview_theme == "light" else '#2d2d2d'}; 
                    padding: 16px;
                    border-radius: 6px;
                    overflow: auto;
                }}
                code {{ 
                    font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
                    font-size: 85%;
                }}
                .mermaid {{
                    text-align: center;
                    margin: 20px 0;
                    background: {'white' if self.current_preview_theme == "light" else '#1e1e1e'};
                }}
                table {{
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                th, td {{
                    border: 1px solid {'#ddd' if self.current_preview_theme == "light" else '#3c3c3c'};
                    padding: 8px;
                }}
                th {{
                    background-color: {'#f6f8fa' if self.current_preview_theme == "light" else '#2d2d2d'};
                }}
            </style>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.6.1/mermaid.min.js"></script>
        </head>
        <body>
            {html_content}
            <script>
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: '{self.current_preview_theme}',
                    securityLevel: 'loose'
                }});
            </script>
        </body>
        </html>
        """

        self.web_view.setHtml(html)
def main():
    app = QApplication(sys.argv)
    window = MarkdownMermaidEditor()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

