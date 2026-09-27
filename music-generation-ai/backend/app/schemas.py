from pydantic import BaseModel, Field
from typing import Optional


class GenerateRequest(BaseModel):
    seed_name: str = Field(..., description="One of the available seed names, e.g. 'Seed 1'")
    num_notes: int = Field(default=200, ge=20, le=1000, description="How many new notes to generate")
    temperature: float = Field(default=1.0, ge=0.1, le=2.0, description="Creativity/randomness control")


class GenerateResponse(BaseModel):
    success: bool
    filename: Optional[str] = None
    download_url: Optional[str] = None
    num_notes_generated: Optional[int] = None
    error: Optional[str] = None