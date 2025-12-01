"""Interactive chat session example."""

from ai_cli_assistant.api import build_client, call_api_with_retry, handle_response
from ai_cli_assistant.cli import load_system_prompt
from ai_cli_assistant import config
from rich.console import Console

console = Console()


def main():
    """Demonstrate programmatic chat session."""
    cfg = config.load_config()
    client = build_client()
    system_prompt = load_system_prompt()
    
    conversation_history = []
    
    # Simulate a conversation
    questions = [
        "What is Python?",
        "What are its main features?",
        "Can you show me a simple example?"
    ]
    
    console.print("[bold blue]Starting Chat Session[/]\n")
    
    for question in questions:
        console.print(f"[bold]User:[/] {question}")
        
        # Add to history
        conversation_history.append({"role": "user", "content": question})
        
        # Build context from history
        full_prompt = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in conversation_history]
        )
        
        # Get response
        response = call_api_with_retry(
            client=client,
            model=cfg.default_model,
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=cfg.temperature
        )
        
        response_text = handle_response(response, cfg.default_model)
        
        # Add to history
        conversation_history.append({"role": "assistant", "content": response_text})
        
        console.print(f"[bold green]Assistant:[/] {response_text}\n")


if __name__ == "__main__":
    main()
