"""Conversation history management."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel


class ConversationEntry(BaseModel):
    """A single conversation entry."""

    timestamp: str
    model: str
    prompt: str
    response: str
    tokens_used: Optional[int] = None


def get_history_file(config_path: Optional[str] = None) -> Path:
    """Get the history file path."""
    if config_path:
        path = Path(config_path).expanduser()
    else:
        path = Path.home() / ".ai_assistant_history.jsonl"

    # Create parent directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def log_conversation(
    prompt: str,
    response: str,
    model: str,
    history_file: Optional[str] = None,
    tokens_used: Optional[int] = None,
) -> None:
    """Log a conversation to the history file."""
    entry = ConversationEntry(
        timestamp=datetime.now().isoformat(),
        model=model,
        prompt=prompt,
        response=response,
        tokens_used=tokens_used,
    )

    file_path = get_history_file(history_file)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry.model_dump_json() + "\n")


def load_history(
    history_file: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[ConversationEntry]:
    """Load conversation history from file."""
    file_path = get_history_file(history_file)

    if not file_path.exists():
        return []

    entries = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                entries.append(ConversationEntry(**data))
            except (json.JSONDecodeError, ValueError):
                continue

    if limit:
        return entries[-limit:]
    return entries


def clear_history(history_file: Optional[str] = None) -> None:
    """Clear the conversation history."""
    file_path = get_history_file(history_file)
    if file_path.exists():
        file_path.unlink()


def export_history(
    output_file: Path,
    history_file: Optional[str] = None,
    format: str = "markdown",
) -> None:
    """Export history to a file."""
    entries = load_history(history_file)

    if format == "markdown":
        content = "# AI Assistant Conversation History\n\n"
        for entry in entries:
            content += f"## {entry.timestamp}\n"
            content += f"**Model:** {entry.model}\n\n"
            content += f"**Prompt:**\n{entry.prompt}\n\n"
            content += f"**Response:**\n{entry.response}\n\n"
            content += "---\n\n"
    else:  # json
        content = json.dumps([e.model_dump() for e in entries], indent=2)

    output_file.write_text(content, encoding="utf-8")
