# Banking FAQ Chatbot

A local banking assistant with a FastAPI backend and a React/Vite frontend. It answers FAQ questions with spaCy preprocessing and TF-IDF similarity, offers confidence-based suggestions, and includes EMI and savings calculators.

## Requirements

- Python 3.11 or newer
- Node.js 20 or newer
- Backend dependencies from `backend/requirements.txt`

## Run Locally

From the repository root, start the backend in one terminal:

```powershell
.\backend\venv\Scripts\Activate.ps1
uvicorn backend.app.main:app --reload
```

Start the frontend in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the frontend terminal, normally `http://localhost:5173`.

## Configuration

Copy `frontend/.env.example` to `frontend/.env` when the API is not running at the default local URL. Set `VITE_API_URL` to the complete API base URL.

For deployed backends, set `ALLOWED_ORIGINS` to a comma-separated list of permitted frontend origins.

## Tests and Checks

```powershell
pytest -q
cd frontend
npm run lint
npm run build
```

The API exposes `GET /api/health` and `POST /api/chat`.
