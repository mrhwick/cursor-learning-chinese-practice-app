## Lesson 03: API basics (FastAPI routes + schemas)

### Goal
Understand:
- what an API route is
- how request/response JSON works
- how the UI calls the API

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

