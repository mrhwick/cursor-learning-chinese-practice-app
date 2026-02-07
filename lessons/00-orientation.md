## Lesson 00: Orientation (learning with Cursor)

### Goal
Be able to:
- run the app locally
- make a tiny change and see it in the browser
- ask Cursor for a plan + an explanation

### Concepts you’re practicing
- What a “repo” is (a folder of code + docs)
- What a “terminal” is (where you run commands)
- What a “dev server” is (a program running on your computer that your browser can visit)
- How to use Cursor as a tutor (plan → small steps → explain-back)

### Allowed files
- `docs/CURSOR_PLAYBOOK.md`
- `apps/web/src/ui/App.tsx`

### Definition of Done
- You can run `./scripts/dev.sh` and open `http://localhost:5173`
- You made a small UI text change and can explain how it got there

---

## Agent Contract (paste into Cursor chat)
You are my coding tutor inside Cursor.

Rules:
- Ask 1–3 clarifying questions if anything is ambiguous.
- Prefer small steps. After each step, tell me what changed and why.
- Don’t skip explanations; explain code in plain language.
- End by asking me 2 questions to check understanding.

---

## Tasks

### Task 1: Run the repo
1) Read `docs/ABSOLUTE_BEGINNER.md` (only if you’re new to terminals).
2) Follow `docs/GETTING_STARTED.md`.
3) Run:
   - `./scripts/dev.sh`

What “success” looks like:
- Your terminal shows the API and web dev servers running.
- Your browser opens `http://localhost:5173` and you see the page.

### Task 2: Make a tiny UI change
1) Open `apps/web/src/ui/App.tsx`.
2) Find the sentence that says this is a learning repo.
3) Add your name to that sentence.
4) Save the file and refresh your browser tab.

Explain-back:
- What file did you change?
- What did the browser do when you refreshed?

### Task 3: Ask Cursor to teach you (not just code)
Paste these into Cursor chat:
- “Explain what Vite is in one paragraph.”
- “Explain what `/api/health` is and where it lives.”
- “If I change text in `App.tsx`, why does it show up when I refresh?”

### If you get stuck
- Open `docs/TROUBLESHOOTING.md`.
- If you’re stuck >20 minutes, ask your human guide (see `docs/MENTOR_GUIDE.md`).

