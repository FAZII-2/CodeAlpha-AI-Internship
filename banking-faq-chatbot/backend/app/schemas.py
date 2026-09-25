from typing import Annotated

from pydantic import BaseModel, Field


MessageText = Annotated[str, Field(min_length=1, max_length=500)]


class ChatRequest(BaseModel):
    """What the frontend sends for each user message."""

    message: MessageText
    recent_messages: list[MessageText] = Field(default_factory=list, max_length=5)


class Suggestion(BaseModel):
    question: str
    category: str
    confidence: float


class ChatResponse(BaseModel):
    """What the backend sends back after matching."""

    answer: str
    confidence: float
    matched_question: str | None = None
    category: str | None = None
    is_fallback: bool
    suggestions: list[Suggestion] = Field(default_factory=list)