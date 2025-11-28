#!/usr/bin/env bash
set -euo pipefail

# Quick setup for macOS/Linux

PYTHON_BIN="python3.14"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Error: python3.14 or python3 is required in PATH." >&2
  exit 1
fi

echo "Using Python interpreter: $PYTHON_BIN"
$PYTHON_BIN -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env (add your GEMINI_API_KEY or GOOGLE_API_KEY)."
fi

echo ""
echo "Setup complete."
echo "Next steps:"
echo "  source .venv/bin/activate"
echo "  python assistant.py ask -p \"Hello\" -m \"gemini-2.5-flash\""
