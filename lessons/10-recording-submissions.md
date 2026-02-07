## Lesson 10: In-browser recording + submissions

### Goal
Students can record audio in the browser (MediaRecorder) and submit it as a pronunciation attempt.

### Concepts you’re practicing
- Browser permissions (microphone access)
- MediaRecorder basics (start/stop → blob)
- Uploading a blob to the API

### Allowed files
- `apps/web/src/ui/PhraseCard.tsx` (extend your phrase card)
- `apps/api/chinese_practice/main.py`
- `apps/api/chinese_practice/storage.py`

### Definition of Done
- Record a short clip and see it appear as a submission with playback.
- Explain what happens when you click Start/Stop recording.

---

## Cursor prompts (copy/paste)

- “Explain MediaRecorder in simple terms.”
- “Show me the smallest UI that records audio and uploads it.”
- “If microphone permission is denied, how should the UI behave?”

---

## Tasks

1) Add submission storage (API)
- Add a DB table for `Submission` if you don’t have it yet.
- Add endpoints:
  - `POST /api/phrases/{phrase_id}/submissions` (upload attempt audio)
  - `GET /api/phrases/{phrase_id}/submissions` (list attempts)
  - `GET /api/submissions/{submission_id}/audio` (play audio)

2) Add recording UI (web)
- Add Start/Stop recording buttons.
- On stop, upload the recorded blob to the API.
- Show a list of submissions with `<audio controls>`.

---

## Verify
- Record a clip and see a new submission show up.
- Refresh the page and confirm the submission still exists (DB-backed).

---

## Common stuck points
- Microphone permission: check browser site settings.
- MediaRecorder not supported: try Chrome.

## Explain-back questions
- Where does the recorded audio live before upload?
- What is a “blob”?
- Why do we still validate content type/size on the API?

