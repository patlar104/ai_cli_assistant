"""Backward compatibility wrapper for the AI CLI Assistant.

This file maintains backward compatibility with the old command:
    python assistant.py [command]

For the new package structure, use:
    python -m ai_cli_assistant [command]

Or after installation:
    ai-assistant [command]
"""

import sys
from pathlib import Path

# Add src to path for development
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from ai_cli_assistant.cli import main

if __name__ == "__main__":
    main()
