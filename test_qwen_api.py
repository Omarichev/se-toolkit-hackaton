"""Quick script to test Qwen LLM API configuration.

Usage:
    python test_qwen_api.py          # uses .env.secret
    python test_qwen_api.py --key <your-key>
    python test_qwen_api.py --base-url <url> --model <model>
"""

import argparse
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load secrets
# ---------------------------------------------------------------------------
_env_secret = Path(__file__).parent / ".env.secret"
if _env_secret.exists():
    load_dotenv(_env_secret, override=True)

# ---------------------------------------------------------------------------
# Defaults (overridable via CLI or env vars)
# ---------------------------------------------------------------------------
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen-plus"


def build_client(base_url: str, api_key: str, model: str) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=base_url.rstrip("/") + "/v1" if not base_url.endswith("/v1") else base_url,
        timeout=60.0,
    )


async def test_chat(api_key: str, base_url: str, model: str) -> None:
    endpoint = base_url.rstrip("/") + "/chat/completions"

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello in 5 words or less."},
    ]

    print(f"🔗 Endpoint : {endpoint}")
    print(f"🧠 Model   : {model}")
    print(f"🔑 API Key : {api_key[:8]}..." if len(api_key) > 8 else f"🔑 API Key : {api_key}")
    print("-" * 60)

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
                    "max_tokens": 100,
                },
            )
            response.raise_for_status()
            data = response.json()

            choice = data.get("choices", [{}])[0]
            message = choice.get("message", {})
            content = message.get("content", "")

            print("✅ Success!")
            print(f"📝 Response: {content.strip()!r}")
            print(f"📊 Usage   : {data.get('usage', 'N/A')}")

    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP {e.response.status_code}")
        try:
            detail = e.response.json()
            print(f"   Detail   : {detail}")
        except Exception:
            print(f"   Body     : {e.response.text}")
    except httpx.ConnectError:
        print("❌ ConnectError – cannot reach the base URL")
    except Exception as e:
        print(f"❌ {type(e).__name__}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Test Qwen LLM API")
    parser.add_argument("--key", default=os.getenv("LLM_API_KEY"))
    parser.add_argument("--base-url", default=os.getenv("LLM_API_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model", default=os.getenv("LLM_API_MODEL", DEFAULT_MODEL))
    args = parser.parse_args()

    if not args.key:
        print("❌ No API key provided. Set LLM_API_KEY in .env.secret or pass --key")
        return

    import asyncio

    asyncio.run(test_chat(args.key, args.base_url, args.model))


if __name__ == "__main__":
    main()
