from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.model_loader import music_model
from app.config import OUTPUTS_DIR
from app.routes import generate, health


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading model...")
    music_model.load()
    print("Model ready. Server starting.")
    yield


app = FastAPI(title="Music Generation AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(generate.router)


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = OUTPUTS_DIR / filename

    if not file_path.exists():
        return {"error": "File not found"}, 404

    return FileResponse(
        path=file_path,
        media_type="audio/midi",
        filename=filename,
    )