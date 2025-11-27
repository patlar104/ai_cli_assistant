"""Simple CLI AI assistant using Google Gen AI."""

import os

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from google import genai

# Typer app setup
app = typer.Typer(add_completion=False, help="Ask Google Gen AI from the terminal.")
console = Console()


@app.callback()
def cli() -> None:
    """Top-level CLI group."""
    # This callback exists so Typer always treats the CLI as a command group,
    # keeping `ask` as an explicit subcommand.
    return


def build_client() -> genai.Client:
    """Create a Gen AI client using the API key from the environment."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        console.print(
            Panel.fit(
                "Set GEMINI_API_KEY (preferred) or GOOGLE_API_KEY in the environment or .env file.",
                title="Missing API key",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    try:
        return genai.Client(api_key=api_key)
    except Exception as exc:  # pragma: no cover - defensive catch for SDK setup errors
        console.print(
            Panel.fit(
                f"Failed to initialize Google Gen AI client:\n{exc}",
                title="Initialization Error",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)


@app.command(name="ask")
def ask(
    prompt: str = typer.Option(
        ...,
        "--prompt",
        "-p",
        help="The question or instruction to send to the model.",
        show_default=False,
    ),
    model: str = typer.Option(
        "gemini-2.5-flash",
        "--model",
        "-m",
        help="Model name to use for generation.",
    ),
) -> None:
    """Send a prompt to Google Gen AI and print the response text."""
    client = build_client()

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
    except Exception as exc:
        console.print(
            Panel.fit(
                f"Request failed:\n{exc}",
                title="API Error",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    if not getattr(response, "text", None):
        safety_details = []

        prompt_feedback = getattr(response, "prompt_feedback", None)
        if prompt_feedback:
            block_reason = getattr(prompt_feedback, "block_reason", None)
            if block_reason and "SAFETY" in str(block_reason).upper():
                prompt_ratings = getattr(prompt_feedback, "safety_ratings", None) or []
                for rating in prompt_ratings:
                    category = getattr(rating, "category", "Unknown category")
                    probability = getattr(rating, "probability", "unknown probability")
                    safety_details.append(
                        f"Prompt blocked: {category} ({probability})"
                    )

        for index, candidate in enumerate(getattr(response, "candidates", None) or []):
            finish_reason = getattr(candidate, "finish_reason", None)
            if finish_reason and "SAFETY" in str(finish_reason).upper():
                ratings = getattr(candidate, "safety_ratings", None) or []
                if ratings:
                    for rating in ratings:
                        category = getattr(rating, "category", "Unknown category")
                        probability = getattr(rating, "probability", "unknown probability")
                        safety_details.append(
                            f"Candidate {index + 1} blocked: {category} ({probability})"
                        )
                else:
                    safety_details.append(
                        f"Candidate {index + 1} blocked for safety (no ratings provided)."
                    )

        if safety_details:
            console.print(
                Panel.fit(
                    "\n".join(safety_details),
                    title="Safety Blocked",
                    border_style="red",
                )
            )
        else:
            console.print(
                Panel.fit(
                    "No text returned from the model.",
                    title="Empty Response",
                    border_style="yellow",
                )
            )

        raise typer.Exit(code=1)

    console.print(
        Panel(
            response.text.strip(),
            title=f"Model: {model}",
            border_style="green",
        )
    )


def main() -> None:
    """Entrypoint for Typer CLI."""
    app()


if __name__ == "__main__":
    main()
