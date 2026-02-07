## Lesson 07: Roles + authorization

### Goal
Add “teacher” vs “student” and enforce rules like “only teachers can create phrases.”

### Concepts you’re practicing
- **Authorization**: what a logged-in user is allowed to do
- Why the UI is not “real security” (the API must enforce rules)
- HTTP status codes:
  - 401 = not logged in
  - 403 = logged in but not allowed

### Allowed files
- `apps/api/chinese_practice/main.py`
- `apps/api/chinese_practice/models.py` (if you have it)
- `apps/api/chinese_practice/schemas.py`
- `apps/web/src/ui/App.tsx`

### Definition of Done
- Users have a role: `teacher` or `student`.
- A student attempting a teacher-only action gets 403.
- The UI hides teacher-only controls for students.

---

## Cursor prompts (copy/paste)

- “Explain authentication vs authorization with a simple example from this app.”
- “Show me the smallest change to add a `role` field to users and return it in `/api/me`.”
- “Add a teacher-only check to `POST /api/phrases` and explain why it belongs on the server.”

---

## Tasks

1) Add a role to the user
- Add a `role` field (teacher/student) to your user model/table.
- Ensure signup can set a role (for now), or hardcode one role while learning.

2) Enforce teacher-only phrase creation
- Protect `POST /api/phrases` so only teachers can create.
- Return 403 when a student tries.

3) Update the UI
- When logged in as student, hide the create phrase form.
- When logged in as teacher, show it.

---

## Verify
- Create a teacher account and create a phrase (should work).
- Create a student account and try to create a phrase (should fail with 403).

---

## Explain-back questions
- Where is the “real” security enforcement? (UI or API?)
- Why do we still hide controls in the UI if the API already enforces rules?

