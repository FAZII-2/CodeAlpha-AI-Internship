from pathlib import Path
from music21 import converter, note, chord
from app.config import BASE_DIR, SEQUENCE_LENGTH

SAMPLE_MIDI_DIR = BASE_DIR / "data" / "sample_midi"

SEED_FILES = {
    "Seed 1": "seed1.mid",
    "Seed 2": "seed2.mid",
    "Seed 3": "seed3.mid",
    "Seed 4": "seed4.mid",
    "Seed 5": "seed5.mid",
}


def extract_notes_from_midi(file_path):
    notes = []
    midi = converter.parse(file_path)
    elements = midi.flatten().notes

    for element in elements:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append(".".join(str(n) for n in element.normalOrder))

    return notes


def get_seed_sequence(music_model, seed_name):
    if seed_name not in SEED_FILES:
        raise ValueError(f"Unknown seed name: {seed_name}")

    file_path = SAMPLE_MIDI_DIR / SEED_FILES[seed_name]
    tokens = extract_notes_from_midi(file_path)

    encoded = [
        music_model.note_to_int[t]
        for t in tokens
        if t in music_model.note_to_int
    ]

    if len(encoded) < SEQUENCE_LENGTH:
        raise ValueError(
            f"Seed file {SEED_FILES[seed_name]} too short after filtering: "
            f"got {len(encoded)} usable tokens, need {SEQUENCE_LENGTH}"
        )

    return encoded[:SEQUENCE_LENGTH]


def get_available_seeds():
    return list(SEED_FILES.keys())