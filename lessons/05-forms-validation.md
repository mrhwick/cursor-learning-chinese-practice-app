## Lesson 05: Forms + validation

### Goal
Practice the full loop:
UI form → API request → validation → success/error UI.

### Allowed files
- `apps/web/src/ui/App.tsx`
- `apps/api/chinese_practice/schemas.py`
- `apps/api/chinese_practice/main.py`

### Definition of Done
- You can create a phrase from the UI.
- You can intentionally trigger a validation error and see a helpful message.

---

## Tasks

1) Add an API endpoint:
- `POST /api/phrases` to create a phrase.
Use a request schema (example: `PhraseCreateRequest`) with server-side validation.

2) In the UI, add a simple “Create phrase” form.

3) Make the UI show a friendly error if the API rejects the input.

Explain-back:
- What validation runs in the browser?
- What validation runs on the server?
- Why do we validate on the server even if we validate in the UI?

