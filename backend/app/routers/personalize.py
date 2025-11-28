"""Personalization router for content adaptation and translation."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.personalization_service import PersonalizationService
from app.services.translation_service import TranslationService


router = APIRouter()
personalization_service = PersonalizationService()
translation_service = TranslationService()


class PersonalizeRequest(BaseModel):
    """Request for content personalization."""
    content: str
    chapter_id: str
    user_level: str = "intermediate"  # beginner, intermediate, advanced
    user_background: dict | None = None


class PersonalizeResponse(BaseModel):
    """Response with personalized content."""
    personalized_content: str
    adaptations_made: list[str]


class TranslateRequest(BaseModel):
    """Request for content translation."""
    content: str
    target_language: str = "ur"  # Urdu by default
    preserve_code: bool = True


class TranslateResponse(BaseModel):
    """Response with translated content."""
    translated_content: str
    source_language: str
    target_language: str


@router.post("/adapt", response_model=PersonalizeResponse)
async def personalize_content(request: PersonalizeRequest):
    """
    Personalize chapter content based on user's background.
    
    Adapts explanations, examples, and complexity based on:
    - Experience level (beginner/intermediate/advanced)
    - Programming background
    - Learning goals
    """
    try:
        result = await personalization_service.adapt_content(
            content=request.content,
            user_level=request.user_level,
            user_background=request.user_background
        )
        return PersonalizeResponse(
            personalized_content=result["content"],
            adaptations_made=result["adaptations"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate", response_model=TranslateResponse)
async def translate_content(request: TranslateRequest):
    """
    Translate chapter content to Urdu (or other languages).
    
    Preserves code blocks and technical terms while translating
    explanatory text.
    """
    try:
        result = await translation_service.translate(
            content=request.content,
            target_language=request.target_language,
            preserve_code=request.preserve_code
        )
        return TranslateResponse(
            translated_content=result["translated"],
            source_language="en",
            target_language=request.target_language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported translation languages."""
    return {
        "languages": [
            {"code": "ur", "name": "Urdu", "native_name": "اردو"},
            {"code": "en", "name": "English", "native_name": "English"},
        ]
    }

