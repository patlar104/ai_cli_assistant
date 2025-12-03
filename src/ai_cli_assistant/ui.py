"""User interface utilities using Rich."""

from typing import Optional

from rich.console import Console
from rich.panel import Panel

console = Console()


def print_error(title: str, message: str) -> None:
    """Print an error message in a red panel."""
    console.print(
        Panel.fit(
            message,
            title=title,
            border_style="red",
        )
    )


def print_warning(title: str, message: str) -> None:
    """Print a warning message in a yellow panel."""
    console.print(
        Panel.fit(
            message,
            title=title,
            border_style="yellow",
        )
    )


def print_response(model: str, text: str) -> None:
    """Print the AI response in a green panel."""
    console.print(
        Panel(
            text,
            title=f"Model: {model}",
            border_style="green",
        )
    )


def print_stream(text: str) -> None:
    """Print streaming text."""
    console.print(text, end="")
