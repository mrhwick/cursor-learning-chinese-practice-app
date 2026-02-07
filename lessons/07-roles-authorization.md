## Lesson 07: Roles + authorization

### Goal
Understand and enforce rules like:
- only teachers create phrases
- only classroom owner edits/deletes phrases

### Allowed files
- `apps/api/chinese_practice/auth.py`
- `apps/api/chinese_practice/main.py`
- `apps/web/src/ui/App.tsx`

### Definition of Done
- As a student, you can’t see teacher-only controls.\n
- As a student, API calls that require teacher role return 403.

---

## Tasks

1) Create both a teacher and a student account.\n
2) Join the same classroom.\n
3) Try to create a phrase as the student and confirm it fails.\n
4) Ask Cursor to explain where the authorization checks live.

