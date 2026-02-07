## Lesson 07: Roles + authorization

### Goal
Understand and enforce rules like:
- only teachers create phrases
- only classroom owner edits/deletes phrases

### Allowed files
- `apps/api/chinese_practice/main.py`
- `apps/web/src/ui/App.tsx`

### Definition of Done
- As a student, teacher-only API calls return 403.
- The UI hides teacher-only controls when logged in as a student.

---

## Tasks

1) Add a `role` column to users (`teacher` or `student`).

2) Enforce teacher-only behavior:
- only teachers can create phrases

3) Update the UI to hide the “create phrase” form unless the logged-in user is a teacher.

Explain-back:
- Where is the “real” security enforcement? (UI or API?)
- Why do we still hide controls in the UI even though the API enforces it?

