import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FAQ_DATA_DIR = BASE_DIR / "data" / "faqs"

SPACY_MODEL = "en_core_web_sm"

CONFIDENT_THRESHOLD = 0.55
SUGGESTION_THRESHOLD = 0.30
MAX_SUGGESTIONS = 3

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]