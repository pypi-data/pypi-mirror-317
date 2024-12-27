import pytest
from stefan.utils.command_executor import CommandExecutor

class TestCommandExecutor:
    def test_successful_command(self):
        # Test a simple echo command
        success, output = CommandExecutor.execute("echo Hello World")
        assert success is True
        assert "Hello World" in output

    def test_failed_command(self):
        # Test a non-existent command
        success, output = CommandExecutor.execute("nonexistentcommand")
        assert success is False
        assert "Command 'nonexistentcommand' failed with error" in output

    def test_command_with_arguments(self):
        # Test command with multiple arguments
        success, output = CommandExecutor.execute("python --version")
        assert success is True
        assert "Python" in output

    def test_command_with_spaces(self):
        # Test command with multiple spaces
        success, output = CommandExecutor.execute("echo   \"Hello   World\"")
        assert success is True
        assert "Hello   World" in output
