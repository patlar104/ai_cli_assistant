# AI CLI Assistant (Google Gen AI, Python 3.12+)

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
- Python 3.12+ installed
- Google Gemini API key set as `GEMINI_API_KEY` (preferred) or `GOOGLE_API_KEY` (legacy)

### Install Python 3.12+
- macOS: `brew install python@3.12` (or use pyenv: `brew install pyenv && pyenv install 3.12`)
- Linux: use your package manager if available, or `pyenv install 3.12`
- Windows: install from the [official Python downloads](https://www.python.org/downloads/windows/) or `winget install Python.Python.3.12`

## Setup
```bash
git clone <your-repo>
cd ai_cli_assistant
# or run ./setup.sh to automate the steps below
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
cp .env.example .env
echo "GEMINI_API_KEY=your-api-key-here" >> .env
```

PowerShell (Windows):
```powershell
# or run ./setup.ps1
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install -e .
Copy-Item .env.example .env
Add-Content .env "GEMINI_API_KEY=your-api-key-here"
```

## Usage

### Quick Start

```bash
# Simple question
python assistant.py ask -p "Explain Python lists"

# Interactive chat mode
python assistant.py chat

# Stream responses in real-time
python assistant.py stream -p "Write a long story"
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

### Configuration

You can configure the assistant using a `.aiassistant.yaml` file in your home directory or project root.

Initialize a default config file:
```bash
python assistant.py config --init
```

#### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `default_model` | `gemini-2.5-flash` | The model used when `-m` is not specified. |
| `temperature` | `0.7` | Controls randomness (0.0 = deterministic, 2.0 = creative). |
| `max_tokens` | `2048` | Maximum number of tokens in the response. |
| `enable_history` | `true` | Whether to log conversations to the history file. |
| `history_file` | `~/.ai_assistant_history.jsonl` | Path to the conversation history file. |
| `verbose` | `false` | Enable debug output by default. |
| `stream_by_default` | `false` | Use streaming for all responses automatically. |

Example `.aiassistant.yaml`:
```yaml
default_model: gemini-2.5-pro
temperature: 0.8
max_tokens: 4096
enable_history: true
verbose: false
```

### Examples

#### 1. Code Review & Analysis
Read a file and ask the AI to review it.
```bash
python assistant.py ask -f src/main.py -p "Review this code for potential bugs and security issues."
```

#### 2. Creative Writing
Use a higher temperature for brainstorming or storytelling.
```bash
python assistant.py ask -p "Write a sci-fi story about AI" -t 1.2 -m gemini-2.5-pro
```

#### 3. Data Summarization (Piping)
Pipe output from other commands directly into the assistant.
```bash
cat data.csv | python assistant.py ask -p "Summarize the trends in this CSV data"
```

#### 4. Managing History
Export your conversation history to Markdown for sharing.
```bash
# Export last 20 conversations
python assistant.py history -n 20 --export my_history.md
```

## Troubleshooting FAQ

**Q: I get an "API key not found" error.**
**A:** Ensure you have created a `.env` file with `GEMINI_API_KEY=your_key` and that your virtual environment is activated.

**Q: The model returns "404 Not Found".**
**A:** The model name in your config or command might be incorrect. Run `python assistant.py models` to see the list of available models for your API key.

**Q: I'm getting "429 Resource Exhausted" errors.**
**A:** You have hit the rate limit for the API. Wait a moment before trying again. The `gemini-2.5-flash` model typically has higher rate limits than `pro`.

**Q: How do I debug connection issues?**
**A:** Run any command with the `-v` or `--verbose` flag to see detailed error logs: `python assistant.py -v ask -p "test"`.

## Contributing

We welcome contributions! Please follow these steps:

1.  **Fork the repository** and clone it locally.
2.  **Install development dependencies**:
    ```bash
    pip install -e ".[dev]"
    ```
3.  **Create a branch** for your feature or fix.
4.  **Run tests** to ensure everything is working:
    ```bash
    pytest
    ```
5.  **Lint your code** using `ruff` and `black`:
    ```bash
    ruff check .
    black .
    ```
6.  **Submit a Pull Request** with a clear description of your changes.

## Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all, regardless of gender, sexual orientation, disability, ethnicity, religion, or similar personal characteristic.

Please be kind and courteous. Harassment, hate speech, and disrespectful behavior will not be tolerated.
