## Lesson 06: Authentication (signup/login/logout)

### Goal
Add accounts so the app can know who is using it.

### Concepts you’re practicing
- **Authentication**: proving “who you are”
- **Password hashing**: storing a safe version of the password (never plain text)
- **Session cookies**: how the browser stays logged in between requests

### Allowed files
- `apps/api/chinese_practice/main.py`
- `apps/api/chinese_practice/schemas.py`
- `apps/web/src/ui/App.tsx`
- `apps/web/src/api/client.ts`

### Definition of Done
- You can sign up, log out, and log in again in the browser.
- `GET /api/me` returns your user when logged in, and 401 when logged out.
- You can explain where “logged in” state lives (cookie + server-side session).

---

## Before you code (Cursor prompts)

Copy/paste into Cursor chat:

1) “Make a plan (max 6 steps) and list the files you’ll change. Wait for me to approve.”
2) “Explain authentication vs authorization in 5 bullets.”
3) “Explain what a cookie is in one paragraph.”

---

## Tasks (step by step)

### Task 1: Add a `User` table
If you don’t have a DB yet, go back to Lesson 04 first.

Add a `User` table with at least:
- `id`
- `email`
- `password_hash`

### Task 2: Add API routes
Add these routes:
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/me`

Suggested behavior:
- Signup creates a user, logs them in, returns a public user shape.
- Login verifies the password, logs them in.
- Logout clears the session.
- `/api/me` returns the current logged-in user.

### Task 3: Add sessions (cookie-based)
Use Starlette/FastAPI session middleware (cookie session).

Cursor prompt:
- “Show me exactly where the cookie gets set and how `/api/me` reads it.”

### Task 4: Add a minimal UI
In the UI:
- fields for email + password
- buttons for signup/login/logout
- a small “logged in as …” section

Make sure the UI handles errors (wrong password, invalid email) with a friendly message.

---

## Verify (manual checklist)
- Sign up with a new email.\n
- Refresh the page: you should still be logged in.\n
- Log out.\n
- Log in again.\n

---

## Explain-back questions (answer in your own words)
- Where is the password stored? (exactly what, and where?)
- What does the browser send to prove you are logged in?
- What’s the difference between 401 and 403?

## Common stuck points
- “I can log in but refresh logs me out”: ask Cursor about cookies and fetch credentials.
- “Hashing library errors”: check `docs/TROUBLESHOOTING.md`.

