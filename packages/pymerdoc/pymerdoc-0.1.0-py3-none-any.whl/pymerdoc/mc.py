from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
                             QLabel, QFileDialog, QSplitter, QWidget)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QTimer, pyqtSlot


class MermaidConverterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mermaid Diagram Converter")
        self.setMinimumSize(1000, 600)

        # Get theme from parent
        self.parent_window = parent
        self.is_dark_mode = self.parent_window.theme_manager.get_theme() == "dark"

        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Create a splitter for resizable panes
        splitter = QSplitter()
        layout.addWidget(splitter)

        # Left pane: Editor
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(10)

        # Editor label
        editor_label = QLabel("Mermaid Code:")
        editor_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        editor_layout.addWidget(editor_label)

        # Editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Enter your Mermaid diagram code here...")
        editor_layout.addWidget(self.editor)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.preview_button = QPushButton("Update Preview")
        self.save_svg_button = QPushButton("Save as SVG")
        self.save_png_button = QPushButton("Save as PNG")

        for button in [self.preview_button, self.save_svg_button, self.save_png_button]:
            button_layout.addWidget(button)

        editor_layout.addLayout(button_layout)

        # Right pane: Preview
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(10)

        # Preview label
        preview_label = QLabel("Preview")
        preview_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        preview_layout.addWidget(preview_label)

        # Web view for preview
        self.web_view = QWebEngineView()
        preview_layout.addWidget(self.web_view)

        # Add both panes to splitter
        splitter.addWidget(editor_widget)
        splitter.addWidget(preview_widget)
        splitter.setSizes([400, 600])

        # Set up the HTML template with CDN
        self.html_template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: '{theme}'
                }});
            </script>
            <style>
                body {{ 
                    margin: 0; 
                    padding: 20px;
                    background-color: {bg_color};
                    color: {text_color};
                }}
                #diagram {{ width: 100%; }}
            </style>
        </head>
        <body>
            <div class="mermaid" id="diagram">
{diagram_code}
            </div>
            <script>
                function getSVG() {{
                    const svgElement = document.querySelector("#diagram svg");
                    return svgElement ? svgElement.outerHTML : '';
                }}
            </script>
        </body>
        </html>
        '''

        # Set up sample diagram
        sample_diagram = """graph TD
    A[Start] --> B{Is it?}
    B -- Yes --> C[OK]
    C --> D[Rethink]
    D --> B
    B -- No --> E[End]"""
        self.editor.setText(sample_diagram)

        # Connect signals
        self.preview_button.clicked.connect(self.update_preview)
        self.save_svg_button.clicked.connect(self.save_svg)
        self.save_png_button.clicked.connect(self.save_png)
        self.editor.textChanged.connect(self.start_preview_timer)

        # Setup preview timer for debouncing
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.update_preview)

        # Apply theme
        self.apply_theme()

        # Initial preview
        self.update_preview()

    def apply_theme(self):
        """Apply the current theme to all widgets"""
        is_dark = self.is_dark_mode

        # Colors for dark/light themes
        bg_color = "#2e2e2e" if is_dark else "#ffffff"
        text_color = "#ffffff" if is_dark else "#000000"
        editor_bg = "#3c3c3c" if is_dark else "#ffffff"
        border_color = "#555555" if is_dark else "#cccccc"
        button_bg = "#424242" if is_dark else "#f0f0f0"
        button_hover = "#4f4f4f" if is_dark else "#e0e0e0"
        accent_color = "#3daee9"

        # Dialog style
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
                color: {text_color};
            }}
            QLabel {{
                color: {text_color};
            }}
            QTextEdit {{
                background-color: {editor_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 8px;
            }}
        """)

        # Button style
        button_style = f"""
            QPushButton {{
                background-color: {button_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
                border: 1px solid {accent_color};
            }}
            QPushButton:pressed {{
                background-color: {"#383838" if is_dark else "#d0d0d0"};
            }}
        """

        # Apply button style
        for button in [self.preview_button, self.save_svg_button, self.save_png_button]:
            button.setStyleSheet(button_style)

    def start_preview_timer(self):
        """Start timer for delayed preview update"""
        self.preview_timer.start(1000)  # 1 second delay

    def update_preview(self):
        """Update the preview with current diagram code"""
        diagram_code = self.editor.toPlainText()

        # Set theme-specific colors
        bg_color = "#2e2e2e" if self.is_dark_mode else "#ffffff"
        text_color = "#ffffff" if self.is_dark_mode else "#000000"
        mermaid_theme = "dark" if self.is_dark_mode else "default"

        html_content = self.html_template.format(
            diagram_code=diagram_code,
            theme=mermaid_theme,
            bg_color=bg_color,
            text_color=text_color
        )
        self.web_view.setHtml(html_content)

    @pyqtSlot()
    def save_svg(self):
        """Save the diagram as SVG"""
        self.web_view.page().runJavaScript(
            "getSVG()",
            self._handle_svg_content
        )

    def _handle_svg_content(self, svg_content):
        """Handle the SVG content after JavaScript execution"""
        if svg_content:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save SVG",
                "",
                "SVG files (*.svg)"
            )
            if file_name:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(svg_content)

    def save_png(self):
        """Save the diagram as PNG"""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save PNG",
            "",
            "PNG files (*.png)"
        )
        if file_name:
            self.web_view.grab().save(file_name, 'PNG')