# tests/test_markdown.py
import pytest
from PyQt6.QtWidgets import QApplication
from pymerdoc.main import MarkdownMermaidEditor


@pytest.fixture
def editor(qapp):
    """Create fresh editor instance for each test"""
    return MarkdownMermaidEditor()


def test_markdown_headings(editor, qtbot):
    """Test markdown headings render correctly"""
    test_content = "# Heading 1\n## Heading 2"
    editor.editor.setPlainText(test_content)

    # Force preview update (bypass timer)
    editor.update_preview()

    # Get HTML content
    html = editor.web_view.page().toHtml()

    # The actual check needs to wait for the page to load
    def check_content():
        return ("<h1>Heading 1</h1>" in html and
                "<h2>Heading 2</h2>" in html)

    qtbot.waitUntil(check_content, timeout=2000)


def test_markdown_list(editor, qtbot):
    """Test markdown lists render correctly"""
    test_content = "- Item 1\n- Item 2\n  - Subitem"
    editor.editor.setPlainText(test_content)
    editor.update_preview()

    html = editor.web_view.page().toHtml()
    qtbot.waitUntil(lambda: "<ul>" in html, timeout=2000)
    qtbot.waitUntil(lambda: "<li>Item 1</li>" in html, timeout=2000)


def test_mermaid_diagram(editor, qtbot):
    """Test mermaid diagram gets proper wrapper"""
    test_content = '''```mermaid
graph TD
    A-->B
```'''
    editor.editor.setPlainText(test_content)
    editor.update_preview()

    html = editor.web_view.page().toHtml()
    qtbot.waitUntil(lambda: '<div class="mermaid">' in html, timeout=2000)
    qtbot.waitUntil(lambda: 'graph TD' in html, timeout=2000)


def test_live_preview_updates(editor, qtbot):
    """Test that preview updates when text changes"""
    # Type some text
    editor.editor.setPlainText("Initial text")

    # Wait for debounce timer
    with qtbot.waitSignal(editor.preview_timer.timeout, timeout=2000):
        editor.editor.setPlainText("Updated text")

    # Check that preview updated
    html = editor.web_view.page().toHtml()
    assert "Updated text" in html


def test_markdown_styles(editor, qtbot):
    """Test that markdown styling is applied"""
    test_content = "**Bold** and *Italic*"
    editor.editor.setPlainText(test_content)
    editor.update_preview()

    html = editor.web_view.page().toHtml()
    qtbot.waitUntil(lambda: "<strong>Bold</strong>" in html, timeout=2000)
    qtbot.waitUntil(lambda: "<em>Italic</em>" in html, timeout=2000)