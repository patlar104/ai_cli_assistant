# AI CLI Assistant (Google Gen AI, Python 3.14)

Minimal terminal assistant powered by the official Google Gen AI Python SDK. Works with Python 3.14+ and Typer-based CLI.

## Prerequisites
- Python 3.14+ installed
- Google API key for Gen AI (`GOOGLE_API_KEY`)

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
# Replace with your own key; the default placeholder matches .env.example
echo "GOOGLE_API_KEY=your-api-key-here" >> .env
```

PowerShell (Windows):
```powershell
# or run ./setup.ps1
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
# Replace with your own key; the default placeholder matches .env.example
Add-Content .env "GOOGLE_API_KEY=your-api-key-here"
```

## Usage
```bash
python assistant.py ask -p "Explain Python lists" -m "gemini-2.5-flash"
```
- `-p/--prompt` is required; `-m/--model` is optional (defaults to `gemini-2.5-flash`).

## Troubleshooting
- Missing API key: ensure `.env` contains `GOOGLE_API_KEY` and the virtualenv is activated.
- Request fails: check network connectivity, verify the model name, and confirm the API key has access.
- Rich/typer import errors: reinstall deps inside the virtualenv (`pip install -r requirements.txt`).
- Still stuck: run with `--help` to confirm CLI options and rerun with a simpler prompt.
