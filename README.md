# AI CLI Assistant (Google Gen AI, Python 3.14)

Enhanced terminal assistant powered by the official Google Gen AI Python SDK. Features conversation history, interactive chat, streaming responses, and more.

## ✨ Features

- 🤖 **Multiple Commands**: ask, chat, stream, history, config, models
- 💾 **Conversation History**: Automatic logging with export to Markdown/JSON
- 🔄 **Interactive Chat**: Multi-turn conversations with context
- ⚡ **Streaming**: Real-time response streaming
- 🔧 **Configuration**: YAML-based config file support
- 🔁 **Retry Logic**: Automatic retry with exponential backoff
- 📝 **System Prompts**: Load custom prompts from `prompts/base_prompt.txt`
- 🎛️ **Temperature Control**: Fine-tune response randomness
- 📥 **File Input**: Read prompts from files or stdin
- 🎨 **Rich Output**: Beautiful terminal formatting with Rich

## Prerequisites
- Python 3.14+ installed
- Google Gemini API key set as `GEMINI_API_KEY` (preferred) or `GOOGLE_API_KEY` (legacy)

### Install Python 3.14
- macOS: `brew install python@3.14` (or use pyenv: `brew install pyenv && pyenv install 3.14.0`)
- Linux: use your package manager if available, or `pyenv install 3.14.0`
- Windows: install from the [official Python downloads](https://www.python.org/downloads/windows/) or `winget install Python.Python.3.14`

## Setup
```bash
git clone <your-repo>
cd ai_cli_assistant
# or run ./setup.sh to automate the steps below
python3.14 -m venv .venv  # fallback to python3 if 3.14 is python3
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
echo "GEMINI_API_KEY=your-api-key-here" >> .env
```

PowerShell (Windows):
```powershell
# or run ./setup.ps1
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
Add-Content .env "GEMINI_API_KEY=your-api-key-here"
```

## Usage

### Quick Start

```bash
# Simple question
python assistant.py ask -p "Explain Python lists"

# Use specific model and temperature
python assistant.py ask -p "Write a poem" -m gemini-2.5-pro -t 1.5

# Read prompt from file
python assistant.py ask -f prompt.txt

# Interactive chat mode
python assistant.py chat

# Stream responses in real-time
python assistant.py stream -p "Write a long story"

# View conversation history
python assistant.py history -n 5

# Export history to file
python assistant.py history --export history.md

# List available models
python assistant.py models

# Initialize configuration file
python assistant.py config --init

# Show current configuration
python assistant.py config

# Enable verbose mode for debugging
python assistant.py -v ask -p "Test"
```

### Commands

- **`ask`** - Ask a single question with optional file input or stdin
- **`chat`** - Start interactive chat session with conversation context
- **`stream`** - Stream responses in real-time for long outputs
- **`history`** - View or export conversation history
- **`clear-history`** - Clear all conversation history
- **`config`** - View or initialize configuration
- **`models`** - List all available Gemini models
- **`version`** - Show version information

### Options

#### Global Options
- `-v, --verbose` - Enable verbose output for debugging

#### Ask Command
- `-p, --prompt TEXT` - The question or instruction (can also use stdin or file)
- `-f, --file PATH` - Read prompt from a file
- `-m, --model TEXT` - Model name (default from config)
- `-t, --temperature FLOAT` - Controls randomness 0.0-2.0 (default from config)
- `--no-history` - Don't save this conversation to history

#### Chat Command
- `-m, --model TEXT` - Model name (default from config)
- `-t, --temperature FLOAT` - Controls randomness 0.0-2.0

#### Stream Command
- `-p, --prompt TEXT` - The question or instruction
- `-f, --file PATH` - Read prompt from a file
- `-m, --model TEXT` - Model name (default from config)

#### History Command
- `-n, --limit INT` - Number of recent entries to show (default: 10)
- `-e, --export PATH` - Export history to file (.md or .json)

#### Config Command
- `--init` - Create a default configuration file
- `-p, --path PATH` - Custom path for config file

### Configuration File

Create a `.aiassistant.yaml` file in your home directory or project root:

```yaml
# Default model to use
default_model: gemini-2.5-flash

# Temperature (0.0 = deterministic, 2.0 = very random)
temperature: 0.7

# Maximum tokens in response
max_tokens: 2048

# Enable conversation history logging
enable_history: true

# History file location
history_file: ~/.ai_assistant_history.jsonl

# Verbose output
verbose: false

# Stream by default
stream_by_default: false
```

Initialize with: `python assistant.py config --init`

### System Prompts

Customize the AI's behavior by editing `prompts/base_prompt.txt`. The system prompt is automatically loaded and applied to all requests.

### Examples

```bash
# Pipe input
echo "Explain quantum computing" | python assistant.py ask

# From file
python assistant.py ask -f my_question.txt

# High creativity (high temperature)
python assistant.py ask -p "Write a creative story" -t 1.8

# Deterministic output (low temperature)
python assistant.py ask -p "Calculate 2+2" -t 0.0

# Chat with specific model
python assistant.py chat -m gemini-2.5-pro

# Export last 20 conversations
python assistant.py history -n 20 --export my_history.md
```

## Troubleshooting
- Missing API key: ensure `.env` contains `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) and the virtualenv is activated.
- Request fails: check network connectivity, verify the model name, and confirm the API key has access.
- Rich/typer import errors: reinstall deps inside the virtualenv (`pip install -r requirements.txt`).
- Still stuck: run with `--help` to confirm CLI options and rerun with a simpler prompt.
