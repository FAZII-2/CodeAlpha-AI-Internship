from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODELS_DIR = BASE_DIR / "models"

MODEL_PATH_KERAS = MODELS_DIR / "music_lstm.keras"
MODEL_PATH_H5 = MODELS_DIR / "music_lstm.h5"
MAPPINGS_PATH = MODELS_DIR / "note_mappings.json"

SEQUENCE_LENGTH = 100

OUTPUTS_DIR = BASE_DIR / "outputs" / "generated_samples"