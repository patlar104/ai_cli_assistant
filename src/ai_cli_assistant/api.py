"""API interaction logic for Google Gen AI."""

import os
from typing import Any, Optional

import typer
from dotenv import load_dotenv
from google import genai
from rich.console import Console
from rich.panel import Panel
from tenacity import retry, stop_after_attempt, wait_exponential

console = Console()


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
    except Exception as exc:
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
) -> Any:
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


def handle_response(response: Any, model: str) -> str:
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
