"""Utilities for loading and managing prompts."""

from pathlib import Path


def load_system_prompt() -> str:
    """Load the base system prompt from file."""
    # Assumes prompts are installed relative to the package root
    # Go up two levels from utils/prompts.py to ai_cli_assistant/
    package_root = Path(__file__).parent.parent
    prompt_path = package_root / "prompts" / "base_prompt.txt"
    
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8").strip()
    return ""
