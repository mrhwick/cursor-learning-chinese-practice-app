# Mentor guide (for the human helper)

This repo is designed for a learner + an AI tutor (Cursor) + a human mentor.

## The goal for the mentor

Help the learner build skill, not just ship code.

Good outcomes:
- the learner can explain what changed and why\n
- the learner can predict what will happen before running it\n
- the learner learns a repeatable debugging habit\n

## When to step in

Step in when:
- the learner is stuck >20 minutes\n
- they’re looping (same error, same attempt)\n
- they’re overwhelmed and not learning\n

## How to help without taking over

- Ask 3 questions:
  - “What are you trying to do?”
  - “What did you expect to happen?”
  - “What actually happened (exact error)?”
- Offer one mental model and one next step.\n
- If you touch the keyboard, narrate and then hand back quickly.\n

## “Help request packet” (what to ask the learner to send you)

Ask them to send:
- the goal\n
- the exact error text\n
- the file they think is involved\n
- what they tried\n
- what they think is happening\n

## Suggested mentor moves by lesson type

- **Setup problems**: verify installs (`node -v`, `python3 --version`), then one command at a time.\n
- **Bug**: make a hypothesis, add one log / inspect one response, rerun.\n
- **Concept confusion**: draw a tiny diagram (browser → api → db) and map where the bug lives.\n

