## Lesson 02: React basics (components + state)

### Goal
Practice component decomposition and state:
- extract a component
- pass props
- keep state local where possible

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

## Suggested tasks

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

