# learning-to-code (Cursor-first fullstack)

This repo is a **learning curriculum** that teaches how to use **Cursor + GPT-5.2** to build a real fullstack app: **Chinese Practice Studio** (multi-user, audio practice, feedback).

The goal is that the learner can truthfully say: **“I built this myself, using Cursor as my tutor.”**

## Start here (don’t overthink it)

If you’re learning to code for the first time, the goal for Day 1 is simple:
- run the app
- see it in your browser
- make one tiny change

### If you’re brand new

Start here:
- `docs/ABSOLUTE_BEGINNER.md`
- then `docs/GETTING_STARTED.md`
- then `lessons/00-orientation.md`

### If you have some experience

Go to:
- `docs/GETTING_STARTED.md`
- then `lessons/00-orientation.md`

## What you’re building (the capstone outcome)

Chinese Practice Studio:
- multi-user (teacher + students)\n
- classrooms (invite codes)\n
- phrase practice with **model audio**\n
- student **recordings/submissions**\n
- peer + teacher **feedback**

You will build this step-by-step using the lesson files in `lessons/`.

## How to use the lessons (the workflow)

1. Start with `lessons/00-orientation.md`.
2. Open the lesson file in Cursor.
3. Add the full lesson to chat context (Cursor: **Add to Chat**).
4. Tell the agent: “Follow the Agent Contract in this lesson.”
5. Implement the tasks in small steps. Run and verify after each step.

## Quickstart (macOS) — after you install prerequisites

If you haven’t installed tools yet, use `docs/GETTING_STARTED.md`.

Run the app from the repo root:
- `./scripts/dev.sh`
- Open `http://localhost:5173`

Stop the running dev servers:
- press `Ctrl+C` in the terminal

## Important: Reference implementation rules

This repo may include a `reference/` implementation. It exists to help you **compare** after you attempt a lesson.

Don’t start by copying the reference. You’ll learn faster if you:
- attempt the lesson first
- then compare structure + decisions
- then explain back what changed and why

See `docs/REFERENCE_USAGE.md`.

## Where to get help (when you’re stuck)

- If something breaks: open `docs/TROUBLESHOOTING.md`
- If you see an error: copy the full error message and paste it into Cursor chat
- If you don’t know a word: open `docs/GLOSSARY.md`
- If you’re stuck >20 minutes: ask your human guide (see `docs/MENTOR_GUIDE.md`)

## Repo map (keep this in mind)

- `apps/web/`: learner React UI (Vite)
- `apps/api/`: learner FastAPI backend
- `lessons/`: lesson files to load into Cursor chat context
- `docs/`: guides (Cursor playbook, troubleshooting, capstone spec)
- `checkpoints/`: end-of-lesson expected-state notes (and optional patches)
- `reference/`: optional completed reference implementation

## Commands (you’ll use these most)

- Dev: `./scripts/dev.sh`
- API tests (once deps installed): `./scripts/test_api.sh`
