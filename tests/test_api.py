import pytest
from unittest.mock import Mock, MagicMock
from ai_cli_assistant import api

class DummyClient:
    """Lightweight stand-in for the real SDK client."""
    def __init__(self, api_key=None):
        self.models = Mock()

@pytest.fixture
def mock_client():
    client = MagicMock()
    client.models.generate_content.return_value = Mock(text="Response text")
    return client

@pytest.fixture(autouse=True)
def disable_dotenv(monkeypatch):
    """Prevent .env contents from affecting API key resolution in tests."""
    monkeypatch.setattr(api, "load_dotenv", lambda: None)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

def test_build_client_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(api.genai, "Client", lambda api_key: DummyClient(api_key))
    client = api.build_client()
    assert isinstance(client, DummyClient)

def test_build_client_missing_key():
    with pytest.raises(api.MissingAPIKeyError):
        api.build_client()

def test_build_client_init_error(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    def raise_error(*args, **kwargs):
        raise Exception("Init failed")
    monkeypatch.setattr(api.genai, "Client", raise_error)
    
    with pytest.raises(api.APIError) as exc:
        api.build_client()
    assert "Init failed" in str(exc.value)

def test_call_api_success(mock_client):
    response = api.call_api_with_retry(mock_client, "model", "prompt")
    assert response.text == "Response text"
    mock_client.models.generate_content.assert_called_once()

def test_call_api_with_config(mock_client):
    api.call_api_with_retry(mock_client, "model", "prompt", system_prompt="sys", temperature=0.5)
    _, kwargs = mock_client.models.generate_content.call_args
    assert kwargs["config"]["system_instruction"] == "sys"
    assert kwargs["config"]["temperature"] == 0.5

def test_handle_response_success():
    mock_response = Mock(text="  Hello  ")
    result = api.handle_response(mock_response, "model")
    assert result == "Hello"

def test_handle_response_safety_block():
    mock_response = Mock(text=None)
    mock_response.candidates = []
    mock_response.prompt_feedback.block_reason = "SAFETY"
    mock_response.prompt_feedback.safety_ratings = [
        Mock(category="HARM_CATEGORY_HATE_SPEECH", probability="HIGH")
    ]
    
    with pytest.raises(api.SafetyError) as exc:
        api.handle_response(mock_response, "model")
    assert "HARM_CATEGORY_HATE_SPEECH" in str(exc.value)

def test_handle_response_candidate_safety_block():
    mock_response = Mock(text=None, prompt_feedback=None)
    candidate = Mock(finish_reason="SAFETY")
    candidate.safety_ratings = [
        Mock(category="HARM_CATEGORY_VIOLENCE", probability="MEDIUM")
    ]
    mock_response.candidates = [candidate]
    
    with pytest.raises(api.SafetyError) as exc:
        api.handle_response(mock_response, "model")
    assert "HARM_CATEGORY_VIOLENCE" in str(exc.value)

def test_handle_response_empty():
    mock_response = Mock(text=None, prompt_feedback=None, candidates=[])
    with pytest.raises(api.APIError) as exc:
        api.handle_response(mock_response, "model")
    assert "No text returned" in str(exc.value)
