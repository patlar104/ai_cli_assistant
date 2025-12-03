"""Enhanced CLI AI assistant using Google Gen AI."""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.panel import Panel

from ai_cli_assistant import api, ui
from ai_cli_assistant import config as config_module
from ai_cli_assistant import history as history_module
from ai_cli_assistant.utils import prompts

# Version
__version__ = "2.0.0"

# Typer app setup
app = typer.Typer(
    add_completion=False,
    help="Enhanced AI assistant powered by Google Gen AI.",
)

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
    
    try:
        client = api.build_client()
    except api.APIError as e:
        ui.print_error("Initialization Error", str(e))
        raise typer.Exit(code=1)

    system_prompt = prompts.load_system_prompt()

    # Get prompt from file or option or stdin
    if prompt_file:
        if not prompt_file.exists():
            ui.console.print(f"[red]File not found: {prompt_file}[/]")
            raise typer.Exit(code=1)
        prompt_text = prompt_file.read_text()
    elif prompt:
        prompt_text = prompt
    elif not sys.stdin.isatty():
        prompt_text = sys.stdin.read().strip()
        if not prompt_text:
            ui.console.print("[red]Error: No prompt provided. Use -p, -f, or pipe input.[/]")
            raise typer.Exit(code=1)
    else:
        ui.console.print("[red]Error: No prompt provided. Use -p, -f, or pipe input.[/]")
        raise typer.Exit(code=1)

    # Use config defaults if not specified
    model_name = model or cfg.default_model
    temp = temperature if temperature is not None else cfg.temperature

    if cfg.verbose:
        ui.console.print(f"[dim]Model: {model_name}[/]")
        ui.console.print(f"[dim]Temperature: {temp}[/]")
        if system_prompt:
            ui.console.print("[dim]System prompt loaded[/]")

    try:
        response = api.call_api_with_retry(client, model_name, prompt_text, system_prompt, temp)
        response_text = api.handle_response(response, model_name)
    except api.SafetyError as e:
        ui.print_error("Safety Blocked", str(e))
        raise typer.Exit(code=1)
    except Exception as exc:
        ui.print_error("API Error", f"Request failed:\n{exc}")
        raise typer.Exit(code=1)

    # Display response
    ui.print_response(model_name, response_text)

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
    
    try:
        client = api.build_client()
    except api.APIError as e:
        ui.print_error("Initialization Error", str(e))
        raise typer.Exit(code=1)

    system_prompt = prompts.load_system_prompt()

    model_name = model or cfg.default_model
    temp = temperature if temperature is not None else cfg.temperature

    ui.console.print(
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
            user_input = ui.console.input("\n[bold blue]You:[/] ").strip()

            if user_input.lower() in ["exit", "quit", "q"]:
                ui.console.print("[green]Goodbye![/]")
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
                with ui.console.status("[bold green]Thinking..."):
                    response = api.call_api_with_retry(
                        client, model_name, full_prompt, system_prompt, temp
                    )
                    response_text = api.handle_response(response, model_name)

                # Add response to history
                conversation_history.append({"role": "assistant", "content": response_text})

                ui.console.print(f"\n[bold green]Assistant:[/] {response_text}")

                # Log to history
                if cfg.enable_history:
                    history_module.log_conversation(
                        prompt=user_input,
                        response=response_text,
                        model=model_name,
                        history_file=cfg.history_file,
                    )

            except api.SafetyError as e:
                ui.print_error("Safety Blocked", str(e))
                continue
            except Exception as exc:
                ui.console.print(f"[red]Error: {exc}[/]")
                continue

        except (KeyboardInterrupt, EOFError):
            ui.console.print("\n[green]Goodbye![/]")
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
    
    try:
        client = api.build_client()
    except api.APIError as e:
        ui.print_error("Initialization Error", str(e))
        raise typer.Exit(code=1)

    system_prompt = prompts.load_system_prompt()

    # Get prompt
    if prompt_file:
        if not prompt_file.exists():
            ui.console.print(f"[red]File not found: {prompt_file}[/]")
            raise typer.Exit(code=1)
        prompt_text = prompt_file.read_text()
    elif prompt:
        prompt_text = prompt
    elif not sys.stdin.isatty():
        prompt_text = sys.stdin.read().strip()
        if not prompt_text:
            ui.console.print("[red]Error: No prompt provided. Use -p, -f, or pipe input.[/]")
            raise typer.Exit(code=1)
    else:
        ui.console.print("[red]Error: No prompt provided. Use -p, -f, or pipe input.[/]")
        raise typer.Exit(code=1)

    model_name = model or cfg.default_model

    ui.console.print(f"[dim]Streaming from {model_name}...[/]\n")

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
                ui.print_stream(chunk.text)
                full_response += chunk.text

        ui.console.print("\n")

        # Log to history
        if cfg.enable_history:
            history_module.log_conversation(
                prompt=prompt_text,
                response=full_response,
                model=model_name,
                history_file=cfg.history_file,
            )

    except Exception as exc:
        ui.console.print(f"\n[red]Error: {exc}[/]")
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
        ui.console.print(f"[green]History exported to {export}[/]")
        return

    entries = history_module.load_history(cfg.history_file, limit=limit)

    if not entries:
        ui.console.print("[yellow]No history found.[/]")
        return

    for entry in entries:
        ui.console.print(
            Panel(
                f"[bold]Prompt:[/] {entry.prompt}\n\n[bold]Response:[/] {entry.response}",
                title=f"{entry.timestamp} | {entry.model}",
                border_style="blue",
            )
        )
        ui.console.print()


@app.command(name="clear-history")
def clear_history_cmd() -> None:
    """Clear conversation history."""
    cfg = get_config()

    confirm = typer.confirm("Are you sure you want to clear all history?")
    if confirm:
        history_module.clear_history(cfg.history_file)
        ui.console.print("[green]History cleared.[/]")
    else:
        ui.console.print("[yellow]Cancelled.[/]")


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
            overwrite = typer.confirm(f"Config file already exists at {config_path}. Overwrite?")
            if not overwrite:
                ui.console.print("[yellow]Cancelled.[/]")
                return

        saved_path = config_module.save_default_config(config_path)
        ui.console.print(f"[green]Configuration file created at {saved_path}[/]")
        return

    cfg = get_config()
    config_path = config_module.get_config_path()

    ui.console.print(
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
    try:
        client = api.build_client()
    except api.APIError as e:
        ui.print_error("Initialization Error", str(e))
        raise typer.Exit(code=1)

    try:
        ui.console.print("[bold]Fetching available models...[/]\n")

        # Get models
        models = client.models.list()

        ui.console.print("[bold green]Available Models:[/]\n")

        for model in models:
            model_name = getattr(model, "name", "Unknown")
            display_name = getattr(model, "display_name", model_name)
            description = getattr(model, "description", "No description available")

            ui.console.print(f"[bold cyan]{display_name}[/]")
            ui.console.print(f"  Name: {model_name}")
            ui.console.print(f"  Description: {description}\n")

    except Exception as exc:
        ui.console.print(f"[red]Error fetching models: {exc}[/]")
        raise typer.Exit(code=1)


@app.command(name="version")
def version() -> None:
    """Show version information."""
    ui.console.print(f"[bold green]AI CLI Assistant v{__version__}[/]")


def main() -> None:
    """Entrypoint for Typer CLI."""
    app()


if __name__ == "__main__":
    main()
