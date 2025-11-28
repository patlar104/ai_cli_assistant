"""Enhanced CLI AI assistant using Google Gen AI."""

import os
import sys
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from tenacity import retry, stop_after_attempt, wait_exponential

from google import genai

from ai_cli_assistant import config as config_module
from ai_cli_assistant import history as history_module

# Version
__version__ = "2.0.0"

# Typer app setup
app = typer.Typer(
    add_completion=False,
    help="Enhanced AI assistant powered by Google Gen AI.",
)
console = Console()

# Global config
_config: Optional[config_module.AssistantConfig] = None


def get_config() -> config_module.AssistantConfig:
    """Get or load the global configuration."""
    global _config
    if _config is None:
        _config = config_module.load_config()
    return _config


@app.callback()
def cli(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output for debugging.",
    ),
) -> None:
    """Enhanced AI assistant with conversation history, streaming, and more."""
    global _config
    _config = config_module.load_config()
    if verbose:
        _config.verbose = True


def load_system_prompt() -> str:
    """Load the base system prompt from file."""
    prompt_path = Path(__file__).parent / "prompts" / "base_prompt.txt"
    if prompt_path.exists():
        return prompt_path.read_text().strip()
    return ""


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
    except Exception as exc:  # pragma: no cover
        console.print(
            Panel.fit(
                f"Failed to initialize Google Gen AI client:\n{exc}",
                title="Initialization Error",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    reraise=True,
)
def call_api_with_retry(
    client: genai.Client,
    model: str,
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
) -> any:
    """Call the API with retry logic for transient failures."""
    config_dict = {}
    
    if system_prompt:
        config_dict["system_instruction"] = system_prompt
    
    if temperature is not None:
        config_dict["temperature"] = temperature
    
    return client.models.generate_content(
        model=model,
        contents=prompt,
        config=config_dict if config_dict else None,
    )


def handle_response(response: any, model: str) -> str:
    """Handle API response and extract text or handle errors."""
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
                    safety_details.append(f"Prompt blocked: {category} ({probability})")

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

    return response.text.strip()


@app.command(name="ask")
def ask(
    prompt: Optional[str] = typer.Option(
        None,
        "--prompt",
        "-p",
        help="The question or instruction to send to the model.",
    ),
    prompt_file: Optional[Path] = typer.Option(
        None,
        "--file",
        "-f",
        help="Read prompt from a file.",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="Model name to use for generation.",
    ),
    temperature: Optional[float] = typer.Option(
        None,
        "--temperature",
        "-t",
        help="Controls randomness (0.0-2.0).",
    ),
    no_history: bool = typer.Option(
        False,
        "--no-history",
        help="Don't save this conversation to history.",
    ),
) -> None:
    """Send a prompt to Google Gen AI and print the response text."""
    cfg = get_config()
    client = build_client()
    system_prompt = load_system_prompt()

    # Get prompt from file or option or stdin
    if prompt_file:
        if not prompt_file.exists():
            console.print(f"[red]File not found: {prompt_file}[/]")
            raise typer.Exit(code=1)
        prompt_text = prompt_file.read_text()
    elif prompt:
        prompt_text = prompt
    elif not sys.stdin.isatty():
        prompt_text = sys.stdin.read()
    else:
        console.print("[red]Error: No prompt provided. Use -p, -f, or pipe input.[/]")
        raise typer.Exit(code=1)

    # Use config defaults if not specified
    model_name = model or cfg.default_model
    temp = temperature if temperature is not None else cfg.temperature

    if cfg.verbose:
        console.print(f"[dim]Model: {model_name}[/]")
        console.print(f"[dim]Temperature: {temp}[/]")
        if system_prompt:
            console.print(f"[dim]System prompt loaded[/]")

    try:
        response = call_api_with_retry(
            client, model_name, prompt_text, system_prompt, temp
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

    response_text = handle_response(response, model_name)

    # Display response
    console.print(
        Panel(
            response_text,
            title=f"Model: {model_name}",
            border_style="green",
        )
    )

    # Log to history
    if cfg.enable_history and not no_history:
        history_module.log_conversation(
            prompt=prompt_text,
            response=response_text,
            model=model_name,
            history_file=cfg.history_file,
        )


@app.command(name="chat")
def chat(
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="Model name to use for generation.",
    ),
    temperature: Optional[float] = typer.Option(
        None,
        "--temperature",
        "-t",
        help="Controls randomness (0.0-2.0).",
    ),
) -> None:
    """Start an interactive chat session with the AI."""
    cfg = get_config()
    client = build_client()
    system_prompt = load_system_prompt()

    model_name = model or cfg.default_model
    temp = temperature if temperature is not None else cfg.temperature

    console.print(
        Panel(
            f"[bold green]Chat mode activated![/]\n"
            f"Model: {model_name}\n"
            f"Type [bold]'exit'[/], [bold]'quit'[/], or press [bold]Ctrl+C[/] to exit.",
            title="AI Assistant Chat",
            border_style="blue",
        )
    )

    conversation_history = []

    while True:
        try:
            user_input = console.input("\n[bold blue]You:[/] ").strip()

            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[green]Goodbye![/]")
                break

            if not user_input:
                continue

            # Add to conversation
            conversation_history.append({"role": "user", "content": user_input})

            # Build full context
            full_prompt = "\n".join(
                [f"{msg['role']}: {msg['content']}" for msg in conversation_history]
            )

            try:
                with console.status("[bold green]Thinking..."):
                    response = call_api_with_retry(
                        client, model_name, full_prompt, system_prompt, temp
                    )

                response_text = handle_response(response, model_name)

                # Add response to history
                conversation_history.append(
                    {"role": "assistant", "content": response_text}
                )

                console.print(f"\n[bold green]Assistant:[/] {response_text}")

                # Log to history
                if cfg.enable_history:
                    history_module.log_conversation(
                        prompt=user_input,
                        response=response_text,
                        model=model_name,
                        history_file=cfg.history_file,
                    )

            except Exception as exc:
                console.print(f"[red]Error: {exc}[/]")
                continue

        except (KeyboardInterrupt, EOFError):
            console.print("\n[green]Goodbye![/]")
            break


@app.command(name="stream")
def stream_ask(
    prompt: Optional[str] = typer.Option(
        None,
        "--prompt",
        "-p",
        help="The question or instruction to send to the model.",
    ),
    prompt_file: Optional[Path] = typer.Option(
        None,
        "--file",
        "-f",
        help="Read prompt from a file.",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="Model name to use for generation.",
    ),
) -> None:
    """Stream responses in real-time."""
    cfg = get_config()
    client = build_client()
    system_prompt = load_system_prompt()

    # Get prompt
    if prompt_file:
        if not prompt_file.exists():
            console.print(f"[red]File not found: {prompt_file}[/]")
            raise typer.Exit(code=1)
        prompt_text = prompt_file.read_text()
    elif prompt:
        prompt_text = prompt
    elif not sys.stdin.isatty():
        prompt_text = sys.stdin.read()
    else:
        console.print("[red]Error: No prompt provided. Use -p, -f, or pipe input.[/]")
        raise typer.Exit(code=1)

    model_name = model or cfg.default_model

    console.print(f"[dim]Streaming from {model_name}...[/]\n")

    try:
        config_dict = {}
        if system_prompt:
            config_dict["system_instruction"] = system_prompt

        full_response = ""
        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=prompt_text,
            config=config_dict if config_dict else None,
        ):
            if hasattr(chunk, "text"):
                console.print(chunk.text, end="")
                full_response += chunk.text

        console.print("\n")

        # Log to history
        if cfg.enable_history:
            history_module.log_conversation(
                prompt=prompt_text,
                response=full_response,
                model=model_name,
                history_file=cfg.history_file,
            )

    except Exception as exc:
        console.print(f"\n[red]Error: {exc}[/]")
        raise typer.Exit(code=1)


@app.command(name="history")
def show_history(
    limit: int = typer.Option(
        10,
        "--limit",
        "-n",
        help="Number of recent entries to show.",
    ),
    export: Optional[Path] = typer.Option(
        None,
        "--export",
        "-e",
        help="Export history to a file (markdown or json).",
    ),
) -> None:
    """Show conversation history."""
    cfg = get_config()

    if export:
        fmt = "json" if export.suffix == ".json" else "markdown"
        history_module.export_history(export, cfg.history_file, fmt)
        console.print(f"[green]History exported to {export}[/]")
        return

    entries = history_module.load_history(cfg.history_file, limit=limit)

    if not entries:
        console.print("[yellow]No history found.[/]")
        return

    for entry in entries:
        console.print(
            Panel(
                f"[bold]Prompt:[/] {entry.prompt}\n\n[bold]Response:[/] {entry.response}",
                title=f"{entry.timestamp} | {entry.model}",
                border_style="blue",
            )
        )
        console.print()


@app.command(name="clear-history")
def clear_history_cmd() -> None:
    """Clear conversation history."""
    cfg = get_config()

    confirm = typer.confirm("Are you sure you want to clear all history?")
    if confirm:
        history_module.clear_history(cfg.history_file)
        console.print("[green]History cleared.[/]")
    else:
        console.print("[yellow]Cancelled.[/]")


@app.command(name="config")
def show_config(
    init: bool = typer.Option(
        False,
        "--init",
        help="Create a default configuration file.",
    ),
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Custom path for config file.",
    ),
) -> None:
    """Show or initialize configuration."""
    if init:
        config_path = path or Path.home() / ".aiassistant.yaml"
        if config_path.exists():
            overwrite = typer.confirm(
                f"Config file already exists at {config_path}. Overwrite?"
            )
            if not overwrite:
                console.print("[yellow]Cancelled.[/]")
                return

        saved_path = config_module.save_default_config(config_path)
        console.print(f"[green]Configuration file created at {saved_path}[/]")
        return

    cfg = get_config()
    config_path = config_module.get_config_path()

    console.print(
        Panel(
            f"""[bold]Configuration:[/]
            
Config file: {config_path}
Default model: {cfg.default_model}
Temperature: {cfg.temperature}
Max tokens: {cfg.max_tokens}
History enabled: {cfg.enable_history}
History file: {cfg.history_file}
Verbose: {cfg.verbose}
Stream by default: {cfg.stream_by_default}""",
            title="AI Assistant Configuration",
            border_style="blue",
        )
    )


@app.command(name="models")
def list_models() -> None:
    """List available models."""
    client = build_client()

    try:
        console.print("[bold]Fetching available models...[/]\n")

        # Get models
        models = client.models.list()

        console.print("[bold green]Available Models:[/]\n")

        for model in models:
            model_name = getattr(model, "name", "Unknown")
            display_name = getattr(model, "display_name", model_name)
            description = getattr(model, "description", "No description available")

            console.print(f"[bold cyan]{display_name}[/]")
            console.print(f"  Name: {model_name}")
            console.print(f"  Description: {description}\n")

    except Exception as exc:
        console.print(f"[red]Error fetching models: {exc}[/]")
        raise typer.Exit(code=1)


@app.command(name="version")
def version() -> None:
    """Show version information."""
    console.print(f"[bold green]AI CLI Assistant v{__version__}[/]")


def main() -> None:
    """Entrypoint for Typer CLI."""
    app()


if __name__ == "__main__":
    main()
