"""Chat router for RAG-powered Q&A."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag_service import RAGService


router = APIRouter()
rag_service = RAGService()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str
    selected_text: str | None = None
    chapter_context: str | None = None
    user_level: str = "intermediate"  # beginner, intermediate, advanced


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str
    sources: list[dict] | None = None
    confidence: float = 1.0


@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    Ask a question about the textbook content.
    
    Uses RAG (Retrieval Augmented Generation) to find relevant
    content and generate a contextual answer.
    """
    try:
        # Build context from selected text and chapter
        context = ""
        if request.selected_text:
            context += f"Selected text: {request.selected_text}\n\n"
        if request.chapter_context:
            context += f"Chapter: {request.chapter_context}\n\n"
        
        # Get answer from RAG service
        result = await rag_service.answer_question(
            question=request.question,
            context=context,
            user_level=request.user_level
        )
        
        return ChatResponse(
            answer=result["answer"],
            sources=result.get("sources"),
            confidence=result.get("confidence", 1.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain")
async def explain_selection(request: ChatRequest):
    """
    Explain selected text in simpler terms.
    
    Adapts explanation based on user's experience level.
    """
    if not request.selected_text:
        raise HTTPException(status_code=400, detail="No text selected")
    
    try:
        result = await rag_service.explain_text(
            text=request.selected_text,
            user_level=request.user_level
        )
        return {"explanation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

