## Lesson 03: API basics (FastAPI routes + schemas)

### Goal
Understand:
- what an API route is
- how request/response JSON works
- how auth affects endpoints

### Allowed files
- `apps/api/chinese_practice/main.py`
- `apps/api/chinese_practice/schemas.py`
- `apps/web/src/api/types.ts`

### Definition of Done
- You can explain what `response_model=...` does
- You can point to at least 2 endpoints and describe their inputs/outputs

---

## Tasks

1) In the API, find these routes and explain what they do:
- `GET /api/me`
- `GET /api/classrooms`
- `GET /api/classrooms/{classroom_id}/phrases`

2) Ask Cursor to add a new simple endpoint:\n
- `GET /api/version` → returns `{ "version": "0.1.0" }`\n
Then display it somewhere in the UI.

