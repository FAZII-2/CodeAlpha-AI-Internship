from music21 import stream, note, chord
from app.config import OUTPUTS_DIR
import uuid


def tokens_to_midi(tokens, output_filename=None):
    output_stream = stream.Stream()

    for token in tokens:
        if "." in token:
            chord_notes = token.split(".")
            notes_in_chord = [note.Note(int(n)) for n in chord_notes]
            new_chord = chord.Chord(notes_in_chord)
            output_stream.append(new_chord)
        elif token.isdigit():
            new_note = note.Note(int(token))
            output_stream.append(new_note)
        else:
            new_note = note.Note(token)
            output_stream.append(new_note)

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    if output_filename is None:
        output_filename = f"generated_{uuid.uuid4().hex[:8]}.mid"

    output_path = OUTPUTS_DIR / output_filename
    output_stream.write("midi", fp=str(output_path))

    return output_path