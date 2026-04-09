"""LLM client for text translation.

Uses OpenAI-compatible API to translate between formal and informal text.
"""

import sys
from typing import Any, Literal


SYSTEM_PROMPT_FORMAL_TO_INFORMAL = """You are a helpful assistant that translates formal text into casual, informal English.

Rules:
- Keep the original meaning intact
- Use contractions (don't, can't, it's, etc.)
- Use casual vocabulary and everyday expressions
- Be friendly and conversational
- Use simpler sentence structures
- Add casual filler words when natural (like "yeah", "so", "pretty much")
- Don't be rude or disrespectful
- If the text is already informal, make it even more casual

Examples:
- "I would like to inquire about the status of my order." → "Hey, can you check what's up with my order?"
- "Please be advised that the meeting has been rescheduled." → "Just a heads up — the meeting got moved to a different time."
- "I am writing to express my sincere gratitude for your assistance." → "Thanks a ton for helping me out, really appreciate it!"

Only return the translated text, nothing else."""

SYSTEM_PROMPT_INFORMAL_TO_FORMAL = """You are a helpful assistant that translates casual, informal text into formal, professional English.

Rules:
- Keep the original meaning intact
- Use proper grammar and complete sentences
- Avoid contractions (use "do not" instead of "don't")
- Use formal vocabulary and professional tone
- Use more sophisticated sentence structures
- Be polite and respectful
- Suitable for business emails, official documents, and academic writing

Examples:
- "Hey, what's up with my order?" → "I would like to inquire about the status of my order."
- "Just a heads up — the meeting got moved." → "Please be advised that the meeting has been rescheduled."
- "Thanks a ton for helping me out!" → "I would like to express my sincere gratitude for your assistance."

Only return the translated text, nothing else."""


async def translate_text(
    text: str,
    config: dict[str, str] | None = None,
    direction: Literal["formal_to_informal", "informal_to_formal"] = "formal_to_informal",
) -> str:
    """Translate text between formal and informal styles.

    Args:
        text: The text to translate
        config: Optional config dict with LLM_API_KEY, LLM_API_BASE_URL, LLM_API_MODEL
        direction: Translation direction - "formal_to_informal" or "informal_to_formal"

    Returns:
        The translated text in the target style
    """
    # Load config if not provided
    if config is None:
        try:
            from bot.config import load_config
        except ImportError:
            from config import load_config
        config = load_config()

    api_key = config.get("LLM_API_KEY", "")
    base_url = config.get("LLM_API_BASE_URL", "http://localhost:42005/v1")
    model = config.get("LLM_API_MODEL", "coder-model")

    if not api_key:
        return "[Error: LLM_API_KEY not configured. Please set it in .env.bot.secret]"

    # Select system prompt based on direction
    if direction == "informal_to_formal":
        system_prompt = SYSTEM_PROMPT_INFORMAL_TO_FORMAL
    else:
        system_prompt = SYSTEM_PROMPT_FORMAL_TO_INFORMAL

    # Ensure base_url ends with /v1 or adjust for chat/completions endpoint
    if not base_url.endswith("/v1") and not base_url.endswith("/chat/completions"):
        base_url = base_url.rstrip("/") + "/v1"

    endpoint = base_url.rstrip("/") + "/chat/completions"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000,
                },
            )
            response.raise_for_status()
            data = response.json()

            # Extract response text
            choice = data.get("choices", [{}])[0]
            message = choice.get("message", {})
            content = message.get("content", "")

            return content.strip() if content else "[No response from LLM]"

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "[Error: LLM authentication failed. Check your API key.]"
        return f"[Error: LLM HTTP {e.response.status_code}]"
    except httpx.ConnectError:
        return "[Error: LLM service unreachable. Make sure the LLM proxy is running.]"
    except Exception as e:
        return f"[Error: {type(e).__name__}: {str(e)}]"
