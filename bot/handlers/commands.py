"""Command handlers for slash commands.

Each handler is a function that takes arguments and returns a string response.
"""

from typing import Literal
from services.llm_client import translate_text

# Global state for direction (per-user would be better in production)
_translation_direction: Literal["formal_to_informal", "informal_to_formal"] = "formal_to_informal"


def set_direction(direction: Literal["formal_to_informal", "informal_to_formal"]) -> None:
    """Set the translation direction."""
    global _translation_direction
    _translation_direction = direction


def get_direction() -> Literal["formal_to_informal", "informal_to_formal"]:
    """Get the current translation direction."""
    return _translation_direction


async def handle_start(args: str, config: dict | None = None) -> str:
    """Handle /start command.

    Args:
        args: Any arguments passed after the command (unused for /start)
        config: Bot configuration

    Returns:
        Welcome message
    """
    return """Welcome to the Formalator Bot! 🔄

I translate text between formal and informal styles.

📝 How to use me:
• Send me any text and I'll translate it
• Use /mode formal→informal or informal→formal to switch mode
• Use /translate <text> for explicit translation
• Use /help to see examples

💡 Current mode: Formal → Informal
(Use /mode to switch)"""


async def handle_help(args: str, config: dict | None = None) -> str:
    """Handle /help command.

    Args:
        args: Any arguments passed after the command (unused for /help)
        config: Bot configuration

    Returns:
        Help message with examples
    """
    direction = get_direction()
    if direction == "formal_to_informal":
        examples = """• "I would like to inquire about..." → "Hey, can you check..."
• "Please be advised that..." → "Just a heads up..."
• "I am writing to express my gratitude" → "Thanks a ton for helping me!""""
        mode_desc = "Formal → Informal"
    else:
        examples = """• "Hey, what's up with my order?" → "I would like to inquire about the status of my order."
• "Just a heads up — the meeting got moved." → "Please be advised that the meeting has been rescheduled."
• "Thanks a ton!" → "I would like to express my sincere gratitude.""""
        mode_desc = "Informal → Formal"

    return f"""📖 Bidirectional Text Translator

Current mode: {mode_desc}

Examples:
{examples}

Commands:
/start - Welcome message
/help - Show this help
/mode <direction> - Switch mode (formal→informal or informal→formal)
/translate <text> - Translate specific text

💬 Simply type any message and I'll translate it!"""


async def handle_mode(args: str, config: dict | None = None) -> str:
    """Handle /mode command to switch translation direction.

    Args:
        args: Direction - "formal→informal" or "informal→formal"
        config: Bot configuration

    Returns:
        Confirmation message
    """
    args_lower = args.strip().lower()

    if "informal" in args_lower and "formal" in args_lower:
        if args_lower.index("informal") < args_lower.index("formal"):
            set_direction("informal_to_formal")
            return "🔄 Mode changed: *Informal → Formal*\n\nNow I'll make your casual text formal and professional."
        else:
            set_direction("formal_to_informal")
            return "🔄 Mode changed: *Formal → Informal*\n\nNow I'll make your formal text casual and conversational."
    elif "formal" in args_lower:
        if "to" in args_lower or "→" in args_lower or "->" in args_lower:
            if args_lower.startswith("formal"):
                set_direction("formal_to_informal")
                return "🔄 Mode changed: *Formal → Informal*\n\nNow I'll make your formal text casual and conversational."
            else:
                set_direction("informal_to_formal")
                return "🔄 Mode changed: *Informal → Formal*\n\nNow I'll make your casual text formal and professional."

    return """Please specify the direction:

/mode formal→informal - Make text casual
/mode informal→formal - Make text formal

Or simply:
/mode formal - Switch to formal output
/mode informal - Switch to informal output"""


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

    direction = get_direction()
    result = await translate_text(text, config, direction)

    if direction == "formal_to_informal":
        return f"🔄 *Informal version:*\n\n{result}"
    else:
        return f"🔄 *Formal version:*\n\n{result}"
