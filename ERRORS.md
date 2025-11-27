# Error and Failure Guide

Common issues you may see while using `assistant.py ask` and how to handle them. All fatal errors exit with code `1`.

## CLI usage problems
- **Unexpected argument / missing required option**: Typer shows usage. Fix the command (e.g., include `-p "your prompt"`).

## API key and auth
- **Missing API key**: CLI prints a red error and exits. Add `GEMINI_API_KEY` (preferred) or `GOOGLE_API_KEY` to `.env` and re-run.
- **Invalid/expired key (401/403)**: API error panel shows the auth failure. Regenerate the key or check permissions.
- **Wrong project/permissions (403 PERMISSION_DENIED)**: Ensure the key has access to the chosen model.

## Model issues
- **Model not found (404 NOT_FOUND)**: The model string is wrong or unsupported. Use a valid model (e.g., `gemini-2.5-flash`).
- **Model not enabled for method**: Error mentions `generateContent` not supported. Choose a model that supports text generation.

## Quota and rate limits
- **429 RESOURCE_EXHAUSTED / quota exceeded**: Too many requests or quota depleted. Wait, reduce volume, or increase quota.

## Network/transport
- **Timeouts, DNS failures, SSL errors**: Typically show as request exceptions in the API error panel. Check connectivity and retry.

## Response handling
- **Empty response text**: CLI reports “No text returned from the model.” Retry or try a different prompt/model.
- **SDK initialization errors**: Initialization panel shows failure (e.g., missing dependencies, incompatible version). Reinstall deps with `pip install -r requirements.txt`.

## Tips
- Run `python assistant.py --help` to verify available commands and options.
- Keep `.venv` active so required packages (typer, rich, google-genai) are available.
- If errors persist, try a simpler prompt and a known-good model: `python assistant.py ask -p "Hello" -m "gemini-2.5-flash"`.
