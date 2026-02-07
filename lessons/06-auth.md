## Lesson 06: Authentication (signup/login/logout)

### Goal
Understand sessions and why we use cookies for this app.

### Allowed files
- `apps/api/chinese_practice/main.py`
- `apps/web/src/ui/App.tsx`
- `apps/web/src/api/client.ts`

### Definition of Done
- You can sign up, log out, and log in again.
- You can explain where “logged in” state lives (cookie + server-side session).

---

## Tasks

1) Add a `User` table in the DB (email + password hash).

2) Add API routes:
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/me`

3) Add cookie-based sessions (FastAPI/Starlette middleware).

4) Add a minimal UI for login/signup/logout.

Explain-back questions:
- What does a cookie do?
- What’s the difference between authentication and authorization?

