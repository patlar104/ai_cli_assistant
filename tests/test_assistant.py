from pathlib import Path
import sys

import pytest
import typer

# Ensure the project root is on sys.path for module imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from assistant import build_client


def test_build_client_exits_when_api_key_missing(monkeypatch, capsys):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    with pytest.raises(typer.Exit) as exc_info:
        build_client()

    assert exc_info.value.exit_code == 1

    captured = capsys.readouterr()
    assert "Missing GOOGLE_API_KEY" in captured.out
    # Ensure the error highlighting is printed via Rich console output
    assert "Error:" in captured.out
