# Banking FAQ Chatbot Frontend

This React frontend is built with Vite and Tailwind CSS. It provides the welcome, voice, and chat screens for the Banking FAQ Chatbot API.

## Development

```powershell
npm install
npm run dev
```

The backend should be running separately with `uvicorn backend.app.main:app --reload` from the repository root.

## API URL

The default API URL is `http://127.0.0.1:8000/api`. To use another backend, copy `.env.example` to `.env` and change `VITE_API_URL`.

## Available Scripts

- `npm run dev` starts the Vite development server.
- `npm run build` creates a production build.
- `npm run preview` serves the production build locally.
- `npm run lint` checks the JavaScript and JSX files.
