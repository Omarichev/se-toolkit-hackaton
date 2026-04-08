"""Translation endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.llm_client import translate_text

router = APIRouter()


class TranslationRequest(BaseModel):
    text: str


class TranslationResponse(BaseModel):
    original: str
    translated: str


@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """Translate formal text to informal style."""
    if not request.text.strip():
        return TranslationResponse(original="", translated="")

    result = await translate_text(request.text)
    return TranslationResponse(original=request.text, translated=result)
