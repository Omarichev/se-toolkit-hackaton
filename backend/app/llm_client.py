"""LLM client for text translation.

Uses OpenAI-compatible API to translate between formal and informal text.
"""

import os
from pathlib import Path
from typing import Literal

import httpx
from dotenv import load_dotenv

# Load environment variables
_env_file = Path(__file__).parent.parent.parent / ".env.secret"
if _env_file.exists():
    load_dotenv(_env_file)

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")
LLM_API_MODEL = os.getenv("LLM_API_MODEL", "coder-model")

SYSTEM_PROMPT_FORMAL_TO_INFORMAL = """You are a helpful assistant that rewrites formal text into clear, simple, and conversational English.

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

SYSTEM_PROMPT_INFORMAL_TO_FORMAL = """You are a helpful assistant that rewrites casual, informal text into clear, professional, and formal English.

Rules:
- Keep the original meaning intact
- Use proper grammar and complete sentences
- Avoid contractions (use "do not" instead of "don't", "cannot" instead of "can't")
- Use formal vocabulary and professional tone
- Use more sophisticated sentence structures
- Be polite and respectful
- Suitable for business emails, official documents, and academic writing

Examples:
- "Hey, can you check what's up with my order?" → "I would like to inquire about the status of my order."
- "Just letting you know, the meeting got moved." → "Please be advised that the meeting has been rescheduled."
- "Thanks a ton for helping me out!" → "I would like to express my sincere gratitude for your assistance."
"""


async def translate_text(
    text: str, direction: Literal["formal_to_informal", "informal_to_formal"] = "formal_to_informal"
) -> str:
    """Translate text between formal and informal styles.

    Args:
        text: The text to translate
        direction: Translation direction - "formal_to_informal" or "informal_to_formal"

    Returns:
        The translated text in the target style
    """
    if not LLM_API_KEY:
        return "[Error: LLM_API_KEY not configured]"

    # Select system prompt based on direction
    if direction == "informal_to_formal":
        system_prompt = SYSTEM_PROMPT_INFORMAL_TO_FORMAL
        user_instruction = "Rewrite this in clear, formal, professional English. ONLY output the rewritten text:"
    else:
        system_prompt = SYSTEM_PROMPT_FORMAL_TO_INFORMAL
        user_instruction = "Rewrite this in clear, simple English without slang. ONLY output the rewritten text:"

    base_url = LLM_API_BASE_URL
    if not base_url.endswith("/v1") and not base_url.endswith("/chat/completions"):
        base_url = base_url.rstrip("/") + "/v1"

    endpoint = base_url.rstrip("/") + "/chat/completions"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{user_instruction}\n\n{text}"},
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
