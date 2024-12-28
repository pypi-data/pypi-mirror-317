"""
Test suite for the GUI module.
"""

import pytest
from PyQt6.QtWidgets import QApplication
from jdevtools.jgui import Window, Theme, ResponsiveWidget

@pytest.fixture
def app():
    """Create QApplication instance."""
    return QApplication([])

@pytest.fixture
def window(app):
    """Create Window instance."""
    return Window("Test Window")

def test_window_creation(window):
    """Test window creation."""
    assert window.windowTitle() == "Test Window"
    assert isinstance(window.central_widget, QWidget)

def test_theme_light():
    """Test light theme colors."""
    assert Theme.LIGHT['background'] == '#ECEFF4'
    assert Theme.LIGHT['foreground'] == '#2E3440'
    assert Theme.LIGHT['primary'] == '#5E81AC'

def test_theme_dark():
    """Test dark theme colors."""
    assert Theme.DARK['background'] == '#2E3440'
    assert Theme.DARK['foreground'] == '#ECEFF4'
    assert Theme.DARK['primary'] == '#88C0D0'

def test_add_button(window):
    """Test button addition."""
    clicked = False
    def on_click():
        nonlocal clicked
        clicked = True
    
    button = window.add_button("Test", on_click)
    assert button.text() == "Test"
    button.click()
    assert clicked

def test_add_input(window):
    """Test input field addition."""
    input_field = window.add_input("Test placeholder")
    assert input_field.placeholderText() == "Test placeholder"

def test_add_dropdown(window):
    """Test dropdown addition."""
    items = ["Item 1", "Item 2", "Item 3"]
    dropdown = window.add_dropdown(items)
    assert [dropdown.itemText(i) for i in range(dropdown.count())] == items

def test_add_label(window):
    """Test label addition."""
    label = window.add_label("Test label")
    assert label.text() == "Test label"

def test_theme_switching(window):
    """Test theme switching."""
    window.set_theme("dark")
    assert window.theme == Theme.DARK
    window.set_theme("light")
    assert window.theme == Theme.LIGHT

def test_responsive_widget(app):
    """Test responsive widget behavior."""
    widget = ResponsiveWidget()
    # Test small screen
    widget.resize(500, 400)
    assert widget._layout.direction() == QVBoxLayout.Direction.TopToBottom
    # Test large screen
    widget.resize(800, 600)
    assert widget._layout.direction() == QVBoxLayout.Direction.LeftToRight
