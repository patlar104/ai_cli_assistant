# API Reference

## Command Line Interface

### Global Options

Available for all commands:

```
-v, --verbose    Enable verbose output for debugging
--help           Show help message and exit
```

## Commands

### ask

Send a single prompt to the AI model.

**Usage:**
```bash
ai-assistant ask [OPTIONS]
```

**Options:**
- `-p, --prompt TEXT` - The question or instruction to send
- `-f, --file PATH` - Read prompt from a file
- `-m, --model TEXT` - Model name to use (default: from config)
- `-t, --temperature FLOAT` - Controls randomness 0.0-2.0 (default: from config)
- `--no-history` - Don't save this conversation to history

**Examples:**
```bash
ai-assistant ask -p "What is Python?"
ai-assistant ask -f prompt.txt -m gemini-2.5-pro
ai-assistant ask -p "test" --no-history
```

---

### chat

Start an interactive chat session with conversation context.

**Usage:**
```bash
ai-assistant chat [OPTIONS]
```

**Options:**
- `-m, --model TEXT` - Model name to use (default: from config)
- `-t, --temperature FLOAT` - Controls randomness 0.0-2.0 (default: from config)

**Examples:**
```bash
ai-assistant chat
ai-assistant chat -m gemini-2.5-pro -t 0.9
```

**Interactive Commands:**
- Type your message and press Enter
- Type `exit`, `quit`, or `q` to exit
- Press `Ctrl+C` to exit

---

### stream

Stream responses in real-time for long outputs.

**Usage:**
```bash
ai-assistant stream [OPTIONS]
```

**Options:**
- `-p, --prompt TEXT` - The question or instruction to send
- `-f, --file PATH` - Read prompt from a file
- `-m, --model TEXT` - Model name to use (default: from config)

**Examples:**
```bash
ai-assistant stream -p "Write a long essay"
ai-assistant stream -f essay-prompt.txt
```

---

### history

Show or export conversation history.

**Usage:**
```bash
ai-assistant history [OPTIONS]
```

**Options:**
- `-n, --limit INT` - Number of recent entries to show (default: 10)
- `-e, --export PATH` - Export history to file (.md or .json)

**Examples:**
```bash
ai-assistant history
ai-assistant history -n 20
ai-assistant history --export conversations.md
ai-assistant history --export data.json
```

---

### clear-history

Clear all conversation history.

**Usage:**
```bash
ai-assistant clear-history
```

**Interactive:** Prompts for confirmation before deleting.

---

### config

Show or initialize configuration.

**Usage:**
```bash
ai-assistant config [OPTIONS]
```

**Options:**
- `--init` - Create a default configuration file
- `-p, --path PATH` - Custom path for config file (with --init)

**Examples:**
```bash
ai-assistant config                    # Show current config
ai-assistant config --init             # Create default config
ai-assistant config --init -p ./config.yaml
```

---

### models

List all available Gemini models.

**Usage:**
```bash
ai-assistant models
```

**Output:** Displays model names, display names, and descriptions.

---

### version

Show version information.

**Usage:**
```bash
ai-assistant version
```

## Python API

### Using as a Python Module

```python
# Run as module
python -m ai_cli_assistant ask -p "Hello"

# Import in Python code
from ai_cli_assistant import main

# Call programmatically
import sys
sys.argv = ['ai-assistant', 'ask', '-p', 'What is Python?']
main()
```

### Configuration Module

```python
from ai_cli_assistant import config

# Load configuration
cfg = config.load_config()
print(cfg.default_model)
print(cfg.temperature)

# Save default config
config.save_default_config()

# Get config path
path = config.get_config_path()
```

### History Module

```python
from ai_cli_assistant import history

# Log a conversation
history.log_conversation(
    prompt="What is AI?",
    response="AI is...",
    model="gemini-2.5-flash"
)

# Load history
entries = history.load_history(limit=10)
for entry in entries:
    print(f"{entry.timestamp}: {entry.prompt}")

# Export history
from pathlib import Path
history.export_history(
    output_file=Path("export.md"),
    format="markdown"
)

# Clear history
history.clear_history()
```

### Client Building

```python
from ai_cli_assistant.cli import build_client

# Create API client
client = build_client()

# Use client directly
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello!"
)
print(response.text)
```

## Exit Codes

- `0` - Success
- `1` - Error (API failure, missing key, invalid input, etc.)

## Environment Variables

### Required

- `GEMINI_API_KEY` (preferred) or `GOOGLE_API_KEY` - Your Google AI API key

### Optional

- `AI_ASSISTANT_CONFIG` - Override config file location

## Configuration File Format

See [Configuration Guide](configuration.md) for full details.

```yaml
default_model: gemini-2.5-flash
temperature: 0.7
max_tokens: 2048
enable_history: true
history_file: ~/.ai_assistant_history.jsonl
verbose: false
stream_by_default: false
```

## History File Format

History is stored in JSONL (JSON Lines) format:

```json
{"timestamp": "2025-11-28T10:30:00", "model": "gemini-2.5-flash", "prompt": "Hello", "response": "Hi there!", "tokens_used": null}
```

Each line is a complete JSON object representing one conversation.

## Error Handling

The assistant handles several types of errors:

1. **Missing API Key** - Clear error message with instructions
2. **API Failures** - Retry logic with exponential backoff (3 attempts)
3. **Safety Blocks** - Detailed safety rating information
4. **Invalid Config** - Falls back to defaults with warning
5. **File Not Found** - Clear error for missing prompt files

## Advanced Usage

### Scripting

```bash
#!/bin/bash
# Batch process prompts
for file in prompts/*.txt; do
    ai-assistant ask -f "$file" --no-history
done
```

### Integration

```python
import subprocess
import json

# Call from Python
result = subprocess.run(
    ['ai-assistant', 'ask', '-p', 'What is 2+2?'],
    capture_output=True,
    text=True
)
print(result.stdout)
```

### CI/CD

```yaml
# GitHub Actions example
- name: AI Code Review
  run: |
    ai-assistant ask -f code-changes.diff \
      -p "Review these changes" \
      --no-history
```

## Rate Limits

Google AI API has rate limits. The assistant includes:
- Exponential backoff retry logic
- Clear error messages for rate limit errors

Check [Google AI documentation](https://ai.google.dev) for current limits.

## Support

- [GitHub Issues](https://github.com/patlar104/ai_cli_assistant/issues)
- [Documentation](https://github.com/patlar104/ai_cli_assistant/docs)
