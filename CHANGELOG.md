# Changelog

## [2.0.0] - 2025-12-01

### 🎉 Major Release - Enhanced Features & Refactoring

#### Added
- **Interactive Chat Mode** - Multi-turn conversations with context (`chat` command)
- **Streaming Responses** - Real-time response streaming (`stream` command)
- **Conversation History** - Automatic logging with JSONL format
- **History Management** - View, export (Markdown/JSON), and clear history
- **Configuration System** - YAML-based config file support (`.aiassistant.yaml`)
- **System Prompts** - Load custom prompts from `prompts/base_prompt.txt`
- **Retry Logic** - Automatic retry with exponential backoff using tenacity
- **Temperature Control** - Fine-tune response randomness (0.0-2.0)
- **File Input Support** - Read prompts from files (`-f/--file` option)
- **Stdin Support** - Pipe input directly to the assistant
- **Verbose Mode** - Debug output with `-v/--verbose` flag
- **Models Command** - List all available Gemini models
- **Version Command** - Show version information
- **Config Command** - View and initialize configuration files

#### Enhanced
- **Ask Command** - Now supports file input, stdin, temperature control, and history opt-out
- **Error Handling** - Improved error messages and safety block reporting
- **CLI Interface** - More intuitive command structure with better help text
- **Documentation** - Comprehensive README with examples and usage guide

#### Technical Improvements
- **Refactoring & Modularization** - Moved core logic to `src/ai_cli_assistant/api.py` and adopted `src`-layout.
- **Package Structure** - Moved prompts to `src/ai_cli_assistant/prompts` for better distribution.
- Added `config.py` module for configuration management
- Added `history.py` module for conversation logging
- Integrated Pydantic for data validation
- Added PyYAML for configuration parsing
- Added Tenacity for retry logic
- Added Pygments for syntax highlighting support
- Refactored code into reusable functions
- Improved type hints throughout

#### Dependencies Added
- `pyyaml>=6.0.1` - YAML configuration parsing
- `tenacity>=8.2.0` - Retry logic with exponential backoff
- `pygments>=2.17.0` - Syntax highlighting
- `pydantic>=2.0.0` - Data validation

### Migration Guide from v1.x

1. **Install new dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize configuration (optional):**
   ```bash
   python assistant.py config --init
   ```

3. **Update command usage:**
   - Old: `python assistant.py ask -p "prompt"`
   - New: Same, but now you can also use `-f` for files or pipe stdin

4. **New features to explore:**
   - Try `python assistant.py chat` for interactive sessions
   - Use `python assistant.py history` to view past conversations
   - Run `python assistant.py models` to see available models

### Backwards Compatibility

All existing commands and options from v1.x continue to work. The `-p/--prompt` option for the `ask` command is now optional if you provide input via file (`-f`) or stdin.

## [1.0.0] - Initial Release

- Basic `ask` command
- Google Gen AI integration
- Safety block handling
- Environment variable configuration
- Rich terminal output
