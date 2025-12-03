import pytest
from pathlib import Path
from ai_cli_assistant import config

def test_default_config():
    cfg = config.AssistantConfig()
    assert cfg.default_model == "gemini-2.5-flash"
    assert cfg.temperature == 0.7
    assert cfg.enable_history is True

def test_load_config_defaults(monkeypatch, tmp_path):
    # Ensure no config file exists in cwd or home
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    
    cfg = config.load_config()
    assert cfg.default_model == "gemini-2.5-flash"

def test_load_config_from_file(monkeypatch, tmp_path):
    config_file = tmp_path / ".aiassistant.yaml"
    config_file.write_text("default_model: test-model\ntemperature: 0.1")
    
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    
    cfg = config.load_config()
    assert cfg.default_model == "test-model"
    assert cfg.temperature == 0.1

def test_load_config_invalid(monkeypatch, tmp_path):
    config_file = tmp_path / ".aiassistant.yaml"
    config_file.write_text("invalid: yaml: content: :")
    
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    
    cfg = config.load_config()
    # Should fall back to defaults
    assert cfg.default_model == "gemini-2.5-flash"

def test_save_default_config(tmp_path):
    target_path = tmp_path / "config.yaml"
    saved_path = config.save_default_config(target_path)
    
    assert saved_path.exists()
    content = saved_path.read_text()
    assert "default_model: gemini-2.5-flash" in content
