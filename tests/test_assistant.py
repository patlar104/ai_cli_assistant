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


def test_build_client_raises_error_when_no_keys_found(monkeypatch):
    monkeypatch.setattr(api.genai, "Client", lambda api_key: DummyClient())

    # Now we expect MissingAPIKeyError instead of typer.Exit
    with pytest.raises(api.MissingAPIKeyError) as excinfo:
        api.build_client()

    assert "GEMINI_API_KEY" in str(excinfo.value)
