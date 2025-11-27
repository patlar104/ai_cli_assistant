from pathlib import Path
import sys

import pytest
import typer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import assistant


class DummyClient:
    """Lightweight stand-in for the real SDK client."""


@pytest.fixture(autouse=True)
def disable_dotenv(monkeypatch):
    """Prevent .env contents from affecting API key resolution in tests."""
    monkeypatch.setattr(assistant, "load_dotenv", lambda: None)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)


def test_build_client_prefers_gemini_when_both_keys_set(monkeypatch):
    captured = {}

    def fake_client(api_key):
        captured["api_key"] = api_key
        return DummyClient()

    monkeypatch.setenv("GEMINI_API_KEY", "gemini-secret")
    monkeypatch.setenv("GOOGLE_API_KEY", "google-secret")
    monkeypatch.setattr(assistant.genai, "Client", fake_client)

    client = assistant.build_client()

    assert isinstance(client, DummyClient)
    assert captured["api_key"] == "gemini-secret"


def test_build_client_falls_back_to_google_key(monkeypatch):
    captured = {}

    def fake_client(api_key):
        captured["api_key"] = api_key
        return DummyClient()

    monkeypatch.setenv("GOOGLE_API_KEY", "google-only")
    monkeypatch.setattr(assistant.genai, "Client", fake_client)

    client = assistant.build_client()

    assert isinstance(client, DummyClient)
    assert captured["api_key"] == "google-only"


def test_build_client_exits_when_no_keys_found(monkeypatch, capsys):
    monkeypatch.setattr(assistant.genai, "Client", lambda api_key: DummyClient())

    with pytest.raises(typer.Exit) as excinfo:
        assistant.build_client()

    assert excinfo.value.exit_code == 1
    output = capsys.readouterr().out
    assert "GEMINI_API_KEY" in output
    assert "GOOGLE_API_KEY" in output
