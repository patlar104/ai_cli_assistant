from pathlib import Path
import sys
import pytest
import typer
from ai_cli_assistant import api

class DummyClient:
    """Lightweight stand-in for the real SDK client."""

@pytest.fixture(autouse=True)
def disable_dotenv(monkeypatch):
    """Prevent .env contents from affecting API key resolution in tests."""
    # Patch load_dotenv in the api module where it is used/imported
    monkeypatch.setattr(api, "load_dotenv", lambda: None)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

def test_build_client_prefers_gemini_when_both_keys_set(monkeypatch):
    captured = {}

    def fake_client(api_key):
        captured["api_key"] = api_key
        return DummyClient()

    monkeypatch.setenv("GEMINI_API_KEY", "gemini-secret")
    monkeypatch.setenv("GOOGLE_API_KEY", "google-secret")
    # Patch genai.Client in the api module
    monkeypatch.setattr(api.genai, "Client", fake_client)

    client = api.build_client()

    assert isinstance(client, DummyClient)
    assert captured["api_key"] == "gemini-secret"

def test_build_client_falls_back_to_google_key(monkeypatch):
    captured = {}

    def fake_client(api_key):
        captured["api_key"] = api_key
        return DummyClient()

    monkeypatch.setenv("GOOGLE_API_KEY", "google-only")
    monkeypatch.setattr(api.genai, "Client", fake_client)

    client = api.build_client()

    assert isinstance(client, DummyClient)
    assert captured["api_key"] == "google-only"

def test_build_client_exits_when_no_keys_found(monkeypatch, capsys):
    monkeypatch.setattr(api.genai, "Client", lambda api_key: DummyClient())

    with pytest.raises(typer.Exit) as excinfo:
        api.build_client()

    assert excinfo.value.exit_code == 1
    # We need to capture stdout/stderr to check for the error message
    # The cli uses rich console, which prints to stdout/stderr
    # capsys should capture it.
    output = capsys.readouterr().out
    # The error message in api.py says "Set GEMINI_API_KEY (preferred) or GOOGLE_API_KEY"
    assert "GEMINI_API_KEY" in output
    assert "GOOGLE_API_KEY" in output
