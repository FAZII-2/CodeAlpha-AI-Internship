from fastapi import APIRouter
from app.model_loader import music_model

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": music_model.is_ready(),
    }