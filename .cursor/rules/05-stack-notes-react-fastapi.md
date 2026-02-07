# Stack notes (React + FastAPI)

## Dev setup assumptions

- Web dev server runs at `http://localhost:5173`
- API runs at `http://localhost:8000`
- Vite proxies `/api/*` to the API (same-origin in the browser)

## Auth assumptions

- Cookie-based sessions
- Browser requests that need cookies must use `credentials: "include"`.

## Audio assumptions

- Uploads are validated (content-type prefix `audio/`, size limit).
- Stored locally in dev (`apps/api/uploads/`).

