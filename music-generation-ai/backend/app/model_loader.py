import json
import tensorflow as tf
from app.config import MODEL_PATH_KERAS, MODEL_PATH_H5, MAPPINGS_PATH


class MusicModel:
    def __init__(self):
        self.model = None
        self.note_to_int = None
        self.int_to_note = None
        self.vocab_size = None
        self.sequence_length = None

    def load(self):
        if MODEL_PATH_KERAS.exists():
            print(f"Loading model from {MODEL_PATH_KERAS}")
            self.model = tf.keras.models.load_model(MODEL_PATH_KERAS)
        elif MODEL_PATH_H5.exists():
            print(f"Loading model from {MODEL_PATH_H5}")
            self.model = tf.keras.models.load_model(MODEL_PATH_H5)
        else:
            raise FileNotFoundError(
                "No trained model file found in models/. "
                "Expected music_lstm.keras or music_lstm.h5"
            )

        with open(MAPPINGS_PATH, "r") as f:
            mappings = json.load(f)

        self.note_to_int = mappings["note_to_int"]
        self.int_to_note = {int(k): v for k, v in mappings["int_to_note"].items()}
        self.vocab_size = mappings["vocab_size"]
        self.sequence_length = mappings["sequence_length"]

        print(f"Model loaded successfully. Vocabulary size: {self.vocab_size}")

    def is_ready(self):
        return self.model is not None


music_model = MusicModel()