"""Command handlers for slash commands.

Each handler is a function that takes arguments and returns a string response.
"""

from services.llm_client import translate_text


async def handle_start(args: str, config: dict | None = None) -> str:
    """Handle /start command.

    Args:
        args: Any arguments passed after the command (unused for /start)
        config: Bot configuration

    Returns:
        Welcome message
    """
    return """Welcome to the Formalator Bot! 🔄

I translate formal text into casual, conversational English.

📝 How to use me:
• Send me any formal text and I'll make it casual
• Use /translate <text> for explicit translation
• Use /help to see examples

💡 Just type or paste any text and I'll informalize it for you!"""


async def handle_help(args: str, config: dict | None = None) -> str:
    """Handle /help command.

    Args:
        args: Any arguments passed after the command (unused for /help)
        config: Bot configuration

    Returns:
        Help message with examples
    """
    return """📖 Formal to Informal Translator

Just send me any formal text and I'll make it casual!

Examples:
• "I would like to inquire about..." → "Hey, can you check..."
• "Please be advised that..." → "Just a heads up..."
• "I am writing to express my gratitude" → "Thanks a ton for helping me!"

Commands:
/start - Welcome message
/help - Show this help
/translate <text> - Translate specific text

💬 Simply type any message and I'll translate it!"""


async def handle_translate(text: str, config: dict | None = None) -> str:
    """Handle /translate command.

    Args:
        text: Text to translate
        config: Bot configuration (contains LLM settings)

    Returns:
        Translated text
    """
    if not text.strip():
        return "Please provide text to translate.\n\nExample: /translate I would like to inquire about my order."

    result = await translate_text(text, config)
    return f"🔄 *Informal version:*\n\n{result}"
