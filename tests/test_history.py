import pytest
import json
from ai_cli_assistant import history

def test_log_conversation(tmp_path):
    history_file = tmp_path / "history.jsonl"
    
    history.log_conversation(
        prompt="Hi",
        response="Hello",
        model="test-model",
        history_file=str(history_file)
    )
    
    assert history_file.exists()
    content = history_file.read_text()
    entry = json.loads(content)
    assert entry["prompt"] == "Hi"
    assert entry["response"] == "Hello"
    assert entry["model"] == "test-model"
    assert "timestamp" in entry

def test_load_history(tmp_path):
    history_file = tmp_path / "history.jsonl"
    # Write two entries
    history.log_conversation("p1", "r1", "m1", str(history_file))
    history.log_conversation("p2", "r2", "m1", str(history_file))
    
    entries = history.load_history(str(history_file))
    assert len(entries) == 2
    assert entries[0].prompt == "p1"
    assert entries[1].prompt == "p2"

def test_load_history_limit(tmp_path):
    history_file = tmp_path / "history.jsonl"
    history.log_conversation("p1", "r1", "m1", str(history_file))
    history.log_conversation("p2", "r2", "m1", str(history_file))
    
    entries = history.load_history(str(history_file), limit=1)
    assert len(entries) == 1
    assert entries[0].prompt == "p2"

def test_clear_history(tmp_path):
    history_file = tmp_path / "history.jsonl"
    history_file.touch()
    
    history.clear_history(str(history_file))
    assert not history_file.exists()

def test_export_history_markdown(tmp_path):
    history_file = tmp_path / "history.jsonl"
    history.log_conversation("p1", "r1", "m1", str(history_file))
    
    export_file = tmp_path / "export.md"
    history.export_history(export_file, str(history_file), format="markdown")
    
    content = export_file.read_text(encoding="utf-8")
    assert "# AI Assistant Conversation History" in content
    assert "**Prompt:**\np1" in content

def test_export_history_json(tmp_path):
    history_file = tmp_path / "history.jsonl"
    history.log_conversation("p1", "r1", "m1", str(history_file))
    
    export_file = tmp_path / "export.json"
    history.export_history(export_file, str(history_file), format="json")
    
    content = export_file.read_text(encoding="utf-8")
    data = json.loads(content)
    assert len(data) == 1
    assert data[0]["prompt"] == "p1"
