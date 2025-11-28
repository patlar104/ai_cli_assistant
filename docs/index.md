# AI CLI Assistant Documentation

Welcome to the AI CLI Assistant documentation!

## Quick Links

- [Installation Guide](installation.md)
- [Usage Examples](usage.md)
- [Configuration Guide](configuration.md)
- [API Reference](api.md)

## Overview

AI CLI Assistant is a powerful command-line tool for interacting with Google's Gemini AI models. It provides:

- **Interactive Chat Mode** - Multi-turn conversations with context
- **Streaming Responses** - Real-time response streaming
- **Conversation History** - Automatic logging and export capabilities
- **Configuration System** - YAML-based configuration
- **System Prompts** - Customizable AI behavior

## Getting Started

```bash
# Install the package
pip install -e .

# Or use directly
python -m ai_cli_assistant ask -p "Hello, AI!"
```

## Features

### Commands

- `ask` - Single-question mode
- `chat` - Interactive conversation mode  
- `stream` - Real-time streaming responses
- `history` - View and export conversation history
- `config` - Manage configuration
- `models` - List available AI models
- `version` - Show version information

### Configuration

Create a `.aiassistant.yaml` file in your home directory or project root:

```yaml
default_model: gemini-2.5-flash
temperature: 0.7
enable_history: true
```

## Support

- [GitHub Issues](https://github.com/patlar104/ai_cli_assistant/issues)
- [GitHub Repository](https://github.com/patlar104/ai_cli_assistant)
