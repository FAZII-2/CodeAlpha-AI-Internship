# Music Generation AI

A deep learning system that generates original piano music using an LSTM neural network trained on the MAESTRO dataset, served through a FastAPI backend and a custom React frontend.

Built as part of the CodeAlpha AI Internship — Task 3.

## Overview

This project trains a 2-layer LSTM on real piano performances (MIDI note sequences), then uses that model to generate new, original music through autoregressive sampling — repeatedly predicting the next note and feeding it back in as context, exactly how text-generation models produce new sentences one word at a time.

## Architecture

├── notebooks/ - Kaggle training notebook (GPU training, dual T4)
├── models/ - Trained LSTM weights + vocabulary mappings
├── data/ - Sample MIDI seed files
├── backend/ - FastAPI inference API (Python)
├── frontend/ - React UI (Vite)
└── outputs/ - Sample generated audio


**Training** happened on Kaggle (dual Tesla T4 GPUs) — the LSTM was trained on 250 MIDI files from the MAESTRO v2.0.0 dataset, using `music21` to convert raw MIDI into note/chord token sequences.

**Inference** runs entirely locally — the trained model is small enough (~5MB) to load and run on CPU, no GPU required for generation.

## Model Details

- **Architecture:** 2-layer LSTM (256 units each) + Dense layers, trained with `sparse_categorical_crossentropy`
- **Vocabulary:** 2,148 unique note/chord tokens
- **Sequence length:** 100 notes of context per prediction
- **Training data:** 250 files from MAESTRO v2.0.0, ~753,000 total tokens, ~728,000 training sequences
- **Training:** ~50 epochs on dual T4 GPUs

## Evaluation

Final training loss: **4.07** — corresponding to a perplexity of **~58.5** across the 2,148-token vocabulary. In plain terms: the model behaves, on average, as if choosing among ~58 plausible candidates per note, compared to random guessing across all 2,148 — a substantial, meaningful improvement.

**Honest limitation:** training loss reflects performance on data the model has seen; it is not a held-out generalization test. Loss and perplexity measure statistical soundness of note-to-note transitions, not subjective musical quality — the real test of generated output is listening to it, which is why sample audio is included in outputs.

## Generation Controls

- **Seed** — 5 curated real musical phrases (pulled from actual MAESTRO recordings) the model continues from
- **Creativity (temperature)** — controls how boldly the model samples from its predictions; lower values stay close to learned patterns, higher values introduce more variation
- **Length** — how many new notes to generate

## Sample Output

Generated samples are available in `outputs/generated_samples/`.

## Running Locally

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` with the backend running at `http://127.0.0.1:8000`.

## Tech Stack

TensorFlow/Keras, FastAPI, music21, React, Vite, Tone.js


## Faizan Ali Ansari