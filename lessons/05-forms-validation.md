## Lesson 05: Forms + validation

### Goal
Practice the full loop:
UI form → API request → validation → success/error UI.

### Concepts you’re practicing
- HTML forms and inputs
- Server-side validation (the API rejects bad input)
- Error handling (showing helpful messages)

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

---

## Cursor prompts (copy/paste)

- “Write the simplest `POST /api/phrases` endpoint with validation and explain each field.”
- “Show me how to display API errors in React without crashing the page.”
- “Give me a small manual test plan: 3 valid cases and 3 invalid cases.”

