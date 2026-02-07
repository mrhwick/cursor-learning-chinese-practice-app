# Troubleshooting

If you’re new: copy the full error message and paste it into Cursor chat.

## Web won’t start (Vite)

- Check you installed deps:
  - `cd apps/web && npm install`
- Check Node version:
  - `node -v` (should be 20+)

## API won’t start (FastAPI)

- Ensure venv exists and deps installed:
  - `cd apps/api`
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install -e ".[dev]"`

## Port already in use

What is a “port”?\n
A port is the `:number` part of a URL (example: `http://localhost:5173`). Two programs can’t usually share the same port.

- Web default: `5173`
- API default: `8000`

Quit the old process or change the port in:
- `apps/web/vite.config.ts`
- `apps/api/run_dev.sh`

## “Not logged in” (401)

Most API routes require a session cookie.

Fix:
- Log in via the UI, then retry.
- Ensure requests include cookies (we use `credentials: "include"` in fetch).

## Audio recording doesn’t work

- Use a browser with MediaRecorder support (Chrome is safest).
- Ensure the page has microphone permission.
- If you see “Invalid content type”, try a different recording format or upload a file.

