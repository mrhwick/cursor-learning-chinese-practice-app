## Lesson 12: Testing + polish

### Goal
Learn how to make changes safely:
- write a failing test
- make it pass
- refactor without breaking behavior

### Concepts you’re practicing
- Tests as “executable requirements”
- Regression prevention (tests catch bugs you already fixed once)
- Why tests are extra important with AI-assisted coding

### Allowed files
- `apps/api/tests/*`
- `apps/api/chinese_practice/main.py`
- `apps/web/src/ui/App.tsx` (optional, if you add a tiny UI polish)

### Definition of Done
- You added at least one meaningful API test.
- You can explain what the test is protecting against.

---

## Cursor prompts (copy/paste)

- “Write a failing test first, then implement the smallest fix.”
- “Explain what this test proves, and what it does NOT prove.”
- “Suggest one refactor that keeps behavior the same, and explain why it’s safe.”

---

## Tasks

1) Add a test for a security/permission rule
Examples (choose one that exists in your current app):
- `/api/me` returns 401 when not logged in
- a student cannot create a classroom (403)
- a non-enrolled user cannot fetch phrase audio (403)

2) Make it pass
- If the test fails, fix the API.
- Keep the fix minimal.

3) Refactor one small thing
- Example: extract a helper function for a repeated “require enrolled” check.
- Re-run tests.

---

## Explain-back questions
- Why is a failing test useful?
- What does “regression” mean?
- What is the smallest change you made to go from red → green?

