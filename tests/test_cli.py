import pytest
from typer.testing import CliRunner
from unittest.mock import Mock, patch
from ai_cli_assistant.cli import app
from ai_cli_assistant import api

runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch("ai_cli_assistant.api.build_client") as mock_build, \
         patch("ai_cli_assistant.api.call_api_with_retry") as mock_call:
        mock_build.return_value = Mock()
        mock_call.return_value = Mock(text="AI Response")
        yield

def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "AI CLI Assistant v" in result.stdout

def test_ask_missing_prompt():
    result = runner.invoke(app, ["ask"])
    assert result.exit_code == 1
    assert "No prompt provided" in result.stdout

def test_ask_with_prompt():
    result = runner.invoke(app, ["ask", "-p", "Hello"])
    assert result.exit_code == 0
    assert "AI Response" in result.stdout

def test_ask_api_error():
    with patch("ai_cli_assistant.api.call_api_with_retry", side_effect=Exception("API Fail")):
        result = runner.invoke(app, ["ask", "-p", "Hello"])
        assert result.exit_code == 1
        assert "API Error" in result.stdout

def test_ask_safety_error():
    with patch("ai_cli_assistant.api.handle_response", side_effect=api.SafetyError("Blocked")):
        result = runner.invoke(app, ["ask", "-p", "Hello"])
        assert result.exit_code == 1
        assert "Safety Blocked" in result.stdout

def test_config_show():
    result = runner.invoke(app, ["config"])
    assert result.exit_code == 0
    assert "Configuration:" in result.stdout

def test_history_empty(tmp_path):
    # Point config to a temp history file
    with patch("ai_cli_assistant.config.load_config") as mock_config:
        mock_config.return_value = Mock(history_file=str(tmp_path / "missing.jsonl"))
        result = runner.invoke(app, ["history"])
        assert result.exit_code == 0
        assert "No history found" in result.stdout

def test_clear_history_abort():
    result = runner.invoke(app, ["clear-history"], input="n\n")
    assert result.exit_code == 0
    assert "Cancelled" in result.stdout
