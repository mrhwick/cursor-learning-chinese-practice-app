## Lesson 03: API basics (FastAPI routes + schemas)

### Goal
Understand:
- what an API route is
- how request/response JSON works
- how the UI calls the API

### Concepts you’re practicing
- FastAPI routes: Python functions that run when a URL is requested
- Response schemas: a “shape” of JSON you promise to return
- `response_model=...`: FastAPI uses this to validate and document responses

### Allowed files
- `apps/api/chinese_practice/main.py`
- `apps/api/chinese_practice/schemas.py`
- `apps/web/src/ui/App.tsx`

### Definition of Done
- You add a new endpoint and use it from the UI.
- You can explain what `response_model=...` does.

---

## Tasks

1) Add a new endpoint:
- `GET /api/version` → returns `{ "version": "0.1.0" }`

2) Create a response schema in `schemas.py` (example: `VersionResponse`).

3) In the UI (`App.tsx`), call `/api/version` and display the version.

4) Explain-back:
- What file contains the API route?
- What file contains the UI code that calls it?
- What is JSON?

---

## Cursor prompts (copy/paste)

- “Implement `GET /api/version` using a pydantic model. Explain what pydantic is.”
- “Show me the smallest diff in `main.py` and `schemas.py`.”
- “Explain `response_model` like I’m new to coding.”

## Mini debugging exercise (optional)

Ask Cursor:
- “How can I make the UI show a friendly message if `/api/version` returns an error?”

