# tests/conftest.py
import pytest
from PyQt6.QtWidgets import QApplication
from pymerdoc.main import MarkdownMermaidEditor

@pytest.fixture(scope='session')
def qapp():
    """Create QApplication instance for tests"""
    app = QApplication([])
    yield app

@pytest.fixture
def editor(qapp):
    """Create fresh editor instance for each test"""
    window = MarkdownMermaidEditor()
    yield window
    window.close()