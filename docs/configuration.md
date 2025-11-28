# Configuration Guide

## Configuration File

The AI CLI Assistant uses YAML configuration files for customization.

### Configuration Locations (Priority Order)

1. Current directory: `./.aiassistant.yaml`
2. Home directory: `~/.aiassistant.yaml`

### Creating Configuration

```bash
# Create default config in home directory
ai-assistant config --init

# Create in custom location
ai-assistant config --init -p /path/to/config.yaml
```

## Configuration Options

### Complete Configuration Example

```yaml
# Default model to use for all commands
default_model: gemini-2.5-flash

# Temperature controls randomness (0.0 = deterministic, 2.0 = very creative)
temperature: 0.7

# Maximum tokens in response (null for no limit)
max_tokens: 2048

# Enable automatic conversation history logging
enable_history: true

# History file location (supports ~ for home directory)
history_file: ~/.ai_assistant_history.jsonl

# Enable verbose output for debugging
verbose: false

# Use streaming by default for all responses
stream_by_default: false
```

### Option Details

#### `default_model`
- **Type**: string
- **Default**: `gemini-2.5-flash`
- **Options**: 
  - `gemini-2.5-flash` - Fast, cost-effective
  - `gemini-2.5-pro` - More capable
  - `gemini-1.5-flash` - Previous generation
  - `gemini-1.5-pro` - Previous generation pro
- **Description**: Model used when `-m/--model` is not specified

#### `temperature`
- **Type**: float (0.0 - 2.0)
- **Default**: 0.7
- **Description**: Controls response randomness
  - 0.0 - 0.3: Focused, deterministic (code, facts)
  - 0.4 - 0.7: Balanced (general use)
  - 0.8 - 1.5: Creative (writing, ideas)
  - 1.6 - 2.0: Very random (experimental)

#### `max_tokens`
- **Type**: integer or null
- **Default**: 2048
- **Description**: Maximum length of responses (null = unlimited)

#### `enable_history`
- **Type**: boolean
- **Default**: true
- **Description**: Automatically log all conversations

#### `history_file`
- **Type**: string (path)
- **Default**: `~/.ai_assistant_history.jsonl`
- **Description**: Location for conversation history

#### `verbose`
- **Type**: boolean
- **Default**: false
- **Description**: Show debug information

#### `stream_by_default`
- **Type**: boolean
- **Default**: false
- **Description**: Use streaming for all responses

## Environment Variables

Environment variables take precedence over configuration files.

### Required Variables

```bash
# API Key (required)
GEMINI_API_KEY=your-api-key-here
# or
GOOGLE_API_KEY=your-api-key-here
```

### Optional Variables

```bash
# Override config file location
AI_ASSISTANT_CONFIG=/path/to/config.yaml
```

## System Prompts

Customize AI behavior by editing prompt templates.

### Base System Prompt

Location: `prompts/base_prompt.txt`

```text
You are a helpful terminal-based AI assistant. Use clear, concise language.
Provide code examples when relevant. Avoid unnecessary verbosity.
```

### Custom Prompts

Create custom prompts for specific use cases:

```bash
# Create a code review prompt
echo "You are a code review expert. Focus on:
- Code quality and best practices
- Security vulnerabilities
- Performance optimization
- Documentation completeness" > prompts/examples/code_review.txt
```

## Command-Line Overrides

Command-line options override both config files and environment variables:

```bash
# Override model
ai-assistant ask -p "test" -m gemini-2.5-pro

# Override temperature
ai-assistant ask -p "test" -t 1.5

# Disable history for one command
ai-assistant ask -p "test" --no-history

# Enable verbose mode
ai-assistant -v ask -p "test"
```

## Configuration Examples

### For Coding Tasks

```yaml
default_model: gemini-2.5-pro
temperature: 0.3
max_tokens: 4096
enable_history: true
```

### For Creative Writing

```yaml
default_model: gemini-2.5-pro
temperature: 1.2
max_tokens: 8192
enable_history: true
```

### For Quick Queries (No History)

```yaml
default_model: gemini-2.5-flash
temperature: 0.7
max_tokens: 1024
enable_history: false
```

### For Development/Testing

```yaml
default_model: gemini-2.5-flash
temperature: 0.5
verbose: true
enable_history: false
```

## Viewing Current Configuration

```bash
# Show all settings and their sources
ai-assistant config
```

Output includes:
- Config file location
- All active settings
- Whether values are default or customized

## Best Practices

1. **Use project-specific configs**:
   - Place `.aiassistant.yaml` in project root
   - Commit to version control (without secrets)

2. **Keep API keys secure**:
   - Never commit `.env` files
   - Use environment variables for secrets

3. **History management**:
   - Regularly export and backup history
   - Use `enable_history: false` for sensitive queries

4. **Model selection**:
   - Use flash models for speed
   - Use pro models for complex tasks

5. **Temperature tuning**:
   - Start at 0.7 and adjust
   - Lower for accuracy, higher for creativity

## Troubleshooting

### Config Not Loading

```bash
# Check which config file is being used
ai-assistant config

# Verify file exists and is valid YAML
cat ~/.aiassistant.yaml
```

### Invalid Configuration

If config file has errors, the application will:
1. Print a warning
2. Fall back to defaults
3. Continue running

### Override Not Working

Command-line options > Environment variables > Config file > Defaults

Check precedence if overrides aren't working.

## Next Steps

- Explore [Usage Examples](usage.md)
- Check [API Reference](api.md)
