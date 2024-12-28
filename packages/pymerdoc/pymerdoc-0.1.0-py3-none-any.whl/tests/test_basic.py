# tests/test_basic.py
def test_window_creation(editor):
    """Test that we can create the main window"""
    assert editor is not None
    assert editor.windowTitle() == "Documentation Editor"

def test_editor_exists(editor):
    """Test that the editor widget exists"""
    assert editor.editor is not None
    assert editor.web_view is not None

def test_empty_editor(editor):
    """Test that editor starts empty"""
    assert editor.editor.toPlainText() == ""