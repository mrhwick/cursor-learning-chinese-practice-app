## Lesson 11: Feedback + moderation

### Goal
Students and teachers can leave feedback on submissions, and the teacher can moderate.

### Concepts you’re practicing
- Nested resources (feedback belongs to a submission)
- Authorization rules:
  - anyone enrolled can read feedback
  - only the author (or classroom owner) can delete feedback

### Allowed files
- `apps/web/src/ui/PhraseCard.tsx`
- `apps/api/chinese_practice/main.py`
- `apps/api/chinese_practice/models.py`
- `apps/api/chinese_practice/schemas.py`

### Definition of Done
- Leave feedback with tones/clarity scores.
- Delete feedback (as the author or classroom owner).
- Explain where the permission checks happen.

---

## Cursor prompts (copy/paste)

- “Propose the simplest feedback schema: comment + two scores.”
- “Where should we enforce ‘only author or owner can delete’?”
- “Show me how to display feedback under a submission in React.”

---

## Tasks

1) Add DB table
- `Feedback` with:
  - submission_id
  - author_id
  - comment
  - score_tones (1–5)
  - score_clarity (1–5)

2) Add API endpoints
- `POST /api/submissions/{submission_id}/feedback`
- `GET /api/submissions/{submission_id}/feedback`
- `DELETE /api/feedback/{feedback_id}`

3) Add UI
- Under each submission:
  - show feedback list
  - a small form to leave feedback
  - a delete button (only when allowed)

---

## Verify
- Student leaves feedback on a submission.
- Teacher can delete feedback for moderation.
- A random non-enrolled user cannot access it.

---

## Explain-back questions
- What is the difference between “feedback author” and “submission owner”?
- Where is moderation enforced, and why?

