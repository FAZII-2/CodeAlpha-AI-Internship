from fastapi import APIRouter, HTTPException
from app.schemas import GenerateRequest, GenerateResponse
from app.model_loader import music_model
from app.generator import generate_notes
from app.midi_converter import tokens_to_midi
from app.seeds import get_seed_sequence, get_available_seeds

router = APIRouter()


@router.get("/seeds")
def list_seeds():
    return {"seeds": get_available_seeds()}


@router.post("/generate", response_model=GenerateResponse)
def generate_music(request: GenerateRequest):
    if not music_model.is_ready():
        raise HTTPException(status_code=503, detail="Model is not loaded yet")

    try:
        seed = get_seed_sequence(music_model, request.seed_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    tokens = generate_notes(
        music_model,
        seed,
        num_notes=request.num_notes,
        temperature=request.temperature,
    )

    output_path = tokens_to_midi(tokens)

    return GenerateResponse(
        success=True,
        filename=output_path.name,
        download_url=f"/download/{output_path.name}",
        num_notes_generated=len(tokens),
    )