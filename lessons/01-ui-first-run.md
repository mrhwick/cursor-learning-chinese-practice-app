## Lesson 01: UI first run (React + API health)

### Goal
Understand the smallest fullstack loop:
Browser → React → `fetch("/api/health")` → FastAPI → JSON → UI.

### Concepts you’re practicing
- Frontend vs backend
- HTTP requests (the browser asking the API for data)
- JSON (data format)
- “Proxy” (Vite forwarding `/api/*` to the backend in development)

### Allowed files
- `apps/web/src/ui/App.tsx`
- `apps/web/vite.config.ts`
- `apps/api/chinese_practice/main.py`

### Definition of Done
- The UI shows something like “API OK” (or a clear success message)
- You can explain what the Vite proxy is doing

---

## Tasks

1) Find the API endpoint
- In `apps/api/chinese_practice/main.py`, find the function that handles `GET /api/health`.
- Ask Cursor: “Explain what this endpoint returns, in plain English.”

2) Find the UI code that calls the endpoint
- In `apps/web/src/ui/App.tsx`, find where the UI calls `/api/health`.
- Ask Cursor: “What does `useEffect` do here?”

3) Find the proxy config
- In `apps/web/vite.config.ts`, find the proxy section.
- Ask Cursor: “Why do we proxy `/api` during development?”

4) Mini experiment (safe)
- Temporarily change the UI to call a wrong URL like `/api/health2`.
- Observe what changes in the UI and the terminal logs.
- Undo the change.

Explain-back questions:
- What file contains the backend route?
- What file contains the frontend call?
- What is the Vite proxy doing?

---

## Prompt for Cursor (copy/paste)
I’m doing Lesson 01. Please:
1) Explain the request flow from browser → React → API in 5 bullets.
2) Show me the smallest code locations for (a) backend endpoint and (b) frontend fetch.
3) Give me one tiny refactor that improves error handling without adding complexity.

