"""Translation endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

from app.llm_client import translate_text

router = APIRouter()


class TranslationRequest(BaseModel):
    text: str
    direction: Literal["formal_to_informal", "informal_to_formal"] = "formal_to_informal"


class TranslationResponse(BaseModel):
    original: str
    translated: str
    direction: str


@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """Translate text between formal and informal styles."""
    if not request.text.strip():
        return TranslationResponse(original="", translated="", direction=request.direction)

    result = await translate_text(request.text, request.direction)
    return TranslationResponse(
        original=request.text, translated=result, direction=request.direction
    )
