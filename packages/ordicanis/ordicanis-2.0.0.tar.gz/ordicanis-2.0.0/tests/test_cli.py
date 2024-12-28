"""
Test suite for the CLI module.
"""

import pytest
from jdevtools.jCLI import Commander

def test_commander_creation():
    """Test Commander instance creation."""
    cli = Commander("Test CLI")
    assert cli.name == "Test CLI"
    assert isinstance(cli.commands, dict)

def test_add_command():
    """Test adding commands to Commander."""
    cli = Commander()
    def test_func():
        return "test"
    
    cli.add_command("test", test_func)
    assert "test" in cli.commands
    assert cli.commands["test"]() == "test"

def test_progress_bar():
    """Test progress bar creation."""
    cli = Commander()
    progress = cli.progress("Testing")
    assert progress is not None

def test_table_creation():
    """Test table creation."""
    cli = Commander()
    table = cli.create_table("Test Table")
    assert table.title == "Test Table"

def test_prompt():
    """Test prompt creation."""
    cli = Commander()
    # Mock user input
    with pytest.MonkeyPatch.context() as m:
        m.setattr('builtins.input', lambda _: "test")
        result = cli.prompt("Enter test:")
        assert result == "test"

def test_success_message(capsys):
    """Test success message display."""
    cli = Commander()
    cli.success("Test successful")
    captured = capsys.readouterr()
    assert "Test successful" in captured.out

def test_error_message(capsys):
    """Test error message display."""
    cli = Commander()
    cli.error("Test error")
    captured = capsys.readouterr()
    assert "Test error" in captured.out

def test_warning_message(capsys):
    """Test warning message display."""
    cli = Commander()
    cli.warning("Test warning")
    captured = capsys.readouterr()
    assert "Test warning" in captured.out
