"""Basic usage example for AI CLI Assistant."""

from ai_cli_assistant.api import build_client, call_api_with_retry, handle_response
from ai_cli_assistant import config


def main():
    """Demonstrate basic API usage."""
    # Load configuration
    cfg = config.load_config()
    
    # Build client
    client = build_client()
    
    # Simple question
    prompt = "What are the three laws of robotics?"
    
    print(f"Asking: {prompt}\n")
    
    # Call API
    response = call_api_with_retry(
        client=client,
        model=cfg.default_model,
        prompt=prompt,
        temperature=cfg.temperature
    )
    
    # Handle response
    response_text = handle_response(response, cfg.default_model)
    
    print(f"Response:\n{response_text}")


if __name__ == "__main__":
    main()
