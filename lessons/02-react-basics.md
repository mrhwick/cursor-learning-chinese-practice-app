## Lesson 02: React basics (components + state)

### Goal
Practice component decomposition and state:
- extract a component
- pass props
- keep state local where possible

### Concepts you’re practicing
- Components: reusable UI building blocks
- Props: inputs to a component
- State: data that changes over time and causes re-rendering

### Allowed files
- `apps/web/src/ui/App.tsx`
- `apps/web/src/ui/PhraseCard.tsx` (you will create this)

### Definition of Done
- You can explain:
  - what a component is
  - what props are
  - what state is
- The UI shows a small list of 3–5 “phrases” using a `PhraseCard` component (mock data is fine).

---

## Tasks (step by step)

1) Create `apps/web/src/ui/PhraseCard.tsx`.
- It should accept props like: `chinese`, `pinyin`, `english`.
- It should render them nicely.

2) In `apps/web/src/ui/App.tsx`, create a small array of mock phrases and render a list of `PhraseCard`s.

3) Add one small piece of state to practice React state:
- example: a “Show pinyin” toggle.

4) Explain-back questions:
- What data is passed as props?
- What data is stored in state?
- What happens when state changes?

---

## How to use Cursor to learn this lesson (copy/paste prompts)

- “Before coding: propose the smallest plan and tell me exactly which files will change.”
- “Write `PhraseCard` with the simplest possible props and explain what props are.”
- “Explain why state changes cause React to re-render, in plain English.”
- “Ask me 3 questions to check that I understand props vs state.”

## Common stuck points

- “I created the component but nothing shows”: usually the component is not imported/used in `App.tsx`.
- “TypeScript error”: ask Cursor to explain the error message and how to fix it without changing unrelated code.

