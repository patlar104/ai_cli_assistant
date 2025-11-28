"""Configuration management for the AI assistant."""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class AssistantConfig(BaseModel):
    """Configuration settings for the AI assistant."""

    default_model: str = Field(default="gemini-2.5-flash")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=2048)
    enable_history: bool = Field(default=True)
    history_file: str = Field(default="~/.ai_assistant_history.jsonl")
    verbose: bool = Field(default=False)
    stream_by_default: bool = Field(default=False)


def get_config_path() -> Path:
    """Get the path to the configuration file."""
    # Check current directory first
    local_config = Path.cwd() / ".aiassistant.yaml"
    if local_config.exists():
        return local_config
    
    # Check home directory
    home_config = Path.home() / ".aiassistant.yaml"
    if home_config.exists():
        return home_config
    
    # Return default location (may not exist)
    return home_config


def load_config() -> AssistantConfig:
    """Load configuration from file or return defaults."""
    config_path = get_config_path()
    
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f) or {}
            return AssistantConfig(**data)
        except Exception:
            # If config is invalid, return defaults
            return AssistantConfig()
    
    return AssistantConfig()


def save_default_config(path: Optional[Path] = None) -> Path:
    """Save a default configuration file."""
    if path is None:
        path = Path.home() / ".aiassistant.yaml"
    
    config = AssistantConfig()
    
    config_content = f"""# AI Assistant Configuration
# See https://github.com/patlar104/ai_cli_assistant for documentation

# Default model to use
default_model: {config.default_model}

# Temperature controls randomness (0.0 = deterministic, 2.0 = very random)
temperature: {config.temperature}

# Maximum tokens in response
max_tokens: {config.max_tokens}

# Enable conversation history logging
enable_history: {config.enable_history}

# History file location
history_file: {config.history_file}

# Verbose output for debugging
verbose: {config.verbose}

# Stream responses by default
stream_by_default: {config.stream_by_default}
"""
    
    path.write_text(config_content)
    return path
