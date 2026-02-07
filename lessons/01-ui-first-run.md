## Lesson 01: UI first run (React + API health)

### Goal
Understand the smallest fullstack loop:
Browser → React → `fetch("/api/health")` → FastAPI → JSON → UI.

### Allowed files
- `apps/web/src/ui/App.tsx`
- `apps/web/vite.config.ts`
- `apps/api/chinese_practice/main.py`

### Definition of Done
- The UI shows something like “API OK” (or a clear success message)
- You can explain what the Vite proxy is doing

---

## Prompt for Cursor
I’m doing Lesson 01. Please:
1) Explain the current request flow from React to FastAPI.
2) Show me where `/api/health` is implemented.
3) Suggest one small improvement to error handling in the UI.

