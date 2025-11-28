# Usage Guide

## Basic Usage

### Ask Command

Send a single question to the AI:

```bash
# Simple question
ai-assistant ask -p "Explain Python lists"

# Use specific model
ai-assistant ask -p "Write a poem" -m gemini-2.5-pro

# Control creativity with temperature
ai-assistant ask -p "Tell me a story" -t 1.5

# Don't save to history
ai-assistant ask -p "Test question" --no-history
```

### Input Methods

#### From Command Line
```bash
ai-assistant ask -p "Your question here"
```

#### From File
```bash
echo "Write a Python function to sort a list" > prompt.txt
ai-assistant ask -f prompt.txt
```

#### From Stdin (Pipe)
```bash
echo "Explain quantum computing" | ai-assistant ask
```

## Interactive Chat Mode

Start a conversation with context:

```bash
ai-assistant chat

# With specific model
ai-assistant chat -m gemini-2.5-pro

# With custom temperature
ai-assistant chat -t 0.9
```

In chat mode:
- Type your messages normally
- Previous messages are remembered
- Type `exit`, `quit`, or press `Ctrl+C` to exit

## Streaming Responses

Get real-time streaming for long responses:

```bash
ai-assistant stream -p "Write a long essay about AI"

# From file
ai-assistant stream -f essay-prompt.txt
```

## Managing History

### View History

```bash
# Show last 10 conversations
ai-assistant history

# Show last 20
ai-assistant history -n 20
```

### Export History

```bash
# Export to Markdown
ai-assistant history --export my-chats.md

# Export to JSON
ai-assistant history --export my-chats.json
```

### Clear History

```bash
ai-assistant clear-history
```

## Configuration Management

### View Current Config

```bash
ai-assistant config
```

### Initialize Config File

```bash
# Create in home directory
ai-assistant config --init

# Create in custom location
ai-assistant config --init -p /path/to/config.yaml
```

## List Available Models

```bash
ai-assistant models
```

## Advanced Usage

### Verbose Mode

Enable debug output:

```bash
ai-assistant -v ask -p "Test"
```

### Custom System Prompts

Edit `prompts/base_prompt.txt` to customize AI behavior:

```text
You are a helpful coding assistant specializing in Python.
Always provide working code examples.
Explain complex concepts simply.
```

### Environment Variables

```bash
# Use different API key temporarily
GEMINI_API_KEY=different-key ai-assistant ask -p "test"
```

## Examples

### Code Generation

```bash
ai-assistant ask -p "Write a Python function to calculate fibonacci numbers"
```

### Code Review

```bash
ai-assistant stream -f my-code.py -p "Review this code and suggest improvements"
```

### Writing Assistant

```bash
ai-assistant chat -t 1.2  # Higher creativity for writing
# Then ask: "Help me write a blog post about AI"
```

### Research Assistant

```bash
ai-assistant ask -p "Summarize the key points about quantum computing" -t 0.3
# Lower temperature for more focused responses
```

### Debugging

```bash
ai-assistant -v ask -f error-log.txt -p "Help me debug this error"
```

## Tips and Best Practices

1. **Use appropriate temperature**:
   - 0.0-0.3: Factual, deterministic (math, code)
   - 0.4-0.7: Balanced (general questions)
   - 0.8-2.0: Creative (stories, brainstorming)

2. **Chat vs Ask**:
   - Use `chat` for multi-turn conversations
   - Use `ask` for single questions

3. **History management**:
   - Export history regularly for backup
   - Clear history to save disk space

4. **Model selection**:
   - `gemini-2.5-flash`: Fast, cost-effective (default)
   - `gemini-2.5-pro`: More capable, slower

5. **File input**:
   - Great for code review, long prompts
   - Can process multiple files with scripting

## Next Steps

- Learn about [Configuration Options](configuration.md)
- Explore [API Reference](api.md)
