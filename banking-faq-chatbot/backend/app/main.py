from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import ALLOWED_ORIGINS
from backend.app.api.routes import router

app = FastAPI(
    title="Banking FAQ Chatbot API",
    description="Matches banking questions to FAQ answers using NLP.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")