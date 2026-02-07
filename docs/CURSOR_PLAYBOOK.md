# Cursor playbook (how to learn fast)

## The loop

1. **Clarify**: “What are we building? What does done mean?”
2. **Plan**: ask for the smallest steps and what files will change.
3. **Implement**: small diffs only.
4. **Run**: verify in browser/tests.
5. **Explain-back**: you explain the code in your own words.

## If you’re new to computers/terminal

Read `docs/ABSOLUTE_BEGINNER.md` first. This repo is designed to assume you’re learning everything from scratch.

## How to use lessons

- Open a lesson in `lessons/`.
- Add the full lesson to chat context.
- Paste: “Follow the Agent Contract in this lesson.”

## Batteries-included Cursor rules

This repo includes Cursor rules under:
- `.cursor/rules/`

They tell the agent to behave like a tutor (small diffs, explain-back, don’t copy from `reference/` by default).

## Agent Contract (default)

You are my coding tutor inside Cursor.

Rules:
- Ask 1–3 clarifying questions before coding if anything is ambiguous.
- Prefer small steps. After each step, tell me what changed and why.
- Don’t skip explanations. After writing code, explain it in plain language.
- Use tests or an explicit manual checklist to define behavior.
- When I’m stuck, debug with me: hypotheses → checks → fix.

Output style:
- Show minimal diffs (only the changed code).
- End with 2 “Explain-back” questions that check my understanding.

## Good prompts

- “Make a plan and list the files you’ll edit. Wait for me to approve.”
- “Show the smallest diff that makes the tests pass.”
- “Explain this function line by line, then ask me what it returns for input X.”
- “We have a bug. Give 3 hypotheses and the fastest way to test each.”

## Anti-patterns to avoid

- “Just write everything for me.” (you won’t learn)
- Copy/paste big blobs without reading them
- Not running the app/tests after changes

## When to ask your human guide

It’s good to struggle a bit, but not forever.

Ask your human guide if:
- you’ve been stuck >20 minutes\n
- you keep hitting the same error\n
- you feel overwhelmed and aren’t learning

See `docs/MENTOR_GUIDE.md` for what information to send them.

