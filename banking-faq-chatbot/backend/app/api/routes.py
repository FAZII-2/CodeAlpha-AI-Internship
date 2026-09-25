from fastapi import APIRouter

from backend.app.schemas import ChatRequest, ChatResponse, Suggestion
from backend.app.nlp.matcher import faq_matcher

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = faq_matcher.match_with_context(
        user_message=request.message,
        recent_messages=request.recent_messages,
    )

    return ChatResponse(
        answer=result.answer,
        confidence=result.confidence,
        matched_question=result.matched_question,
        category=result.category,
        is_fallback=result.is_fallback,
        suggestions=[Suggestion(**s) for s in result.suggestions],
    )


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "faqs_loaded": len(faq_matcher.entries)}