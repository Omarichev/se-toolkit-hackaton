"""LLM client for text translation.

Uses OpenAI-compatible API to translate formal text to informal style.
"""

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Load environment variables
_env_file = Path(__file__).parent.parent.parent / ".env.secret"
if _env_file.exists():
    load_dotenv(_env_file)

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")
LLM_API_MODEL = os.getenv("LLM_API_MODEL", "coder-model")

SYSTEM_PROMPT = """You are a helpful assistant that rewrites formal text into clear, simple, and conversational English.

Rules:
- Keep the original meaning intact
- Use common contractions (don't, can't, it's, etc.)
- Use simple, everyday words that non-native speakers can easily understand
- Be friendly and conversational, but avoid slang, idioms, or regional expressions
- Use shorter, straightforward sentence structures
- Do NOT use filler words like "yeah", "hey", "pretty much", or casual phrases like "cut it", "what's up"
- Keep it polite and clear
- If the text is already simple, just make it slightly more conversational

Examples:
- "I would like to inquire about the status of my order." → "I'd like to check on my order, please."
- "Please be advised that the meeting has been rescheduled." → "Just letting you know, the meeting has been moved to a different time."
- "I am writing to express my sincere gratitude for your assistance." → "Thank you very much for your help, I really appreciate it."
"""


async def translate_text(text: str) -> str:
    """Translate formal text to informal using the LLM API.

    Args:
        text: The formal text to translate

    Returns:
        The informal version of the text
    """
    if not LLM_API_KEY:
        return "[Error: LLM_API_KEY not configured]"

    base_url = LLM_API_BASE_URL
    if not base_url.endswith("/v1") and not base_url.endswith("/chat/completions"):
        base_url = base_url.rstrip("/") + "/v1"

    endpoint = base_url.rstrip("/") + "/chat/completions"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Rewrite this in clear, simple English without slang. ONLY output the rewritten text:\n\n{text}"},
    ]

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {LLM_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": LLM_API_MODEL,
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
