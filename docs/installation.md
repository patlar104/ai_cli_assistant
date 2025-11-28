# Installation Guide

## Prerequisites

- Python 3.14 or higher
- Google Gemini API key

## Installation Methods

### Method 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/patlar104/ai_cli_assistant.git
cd ai_cli_assistant

# Create virtual environment
python3.14 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Method 2: Install from PyPI (When Published)

```bash
pip install ai-cli-assistant
```

### Method 3: Install Production Only

```bash
# Clone and install without dev dependencies
git clone https://github.com/patlar104/ai_cli_assistant.git
cd ai_cli_assistant
pip install .
```

## Configuration

### 1. Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key

### 2. Set Up Environment Variables

Create a `.env` file in your project directory:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
echo "GEMINI_API_KEY=your-api-key-here" >> .env
```

Or set it as an environment variable:

```bash
# Linux/macOS
export GEMINI_API_KEY=your-api-key-here

# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"
```

### 3. Initialize Configuration (Optional)

```bash
ai-assistant config --init
```

This creates a `.aiassistant.yaml` file in your home directory with default settings.

## Verify Installation

```bash
# Check version
ai-assistant version

# Test with a simple question
ai-assistant ask -p "What is 2+2?"
```

## Troubleshooting

### Command not found

If `ai-assistant` command is not found, you can use:

```bash
python -m ai_cli_assistant ask -p "test"
```

### Import errors

Make sure you're in the virtual environment:

```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### API Key Issues

Verify your API key is set:

```bash
# Linux/macOS
echo $GEMINI_API_KEY

# Windows PowerShell
echo $env:GEMINI_API_KEY
```

## Next Steps

- Read the [Usage Guide](usage.md)
- Learn about [Configuration](configuration.md)
- Explore [API Reference](api.md)
