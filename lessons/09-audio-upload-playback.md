## Lesson 09: Audio upload + playback (model audio)

### Goal
Teacher uploads a model audio clip for a phrase; students can play it.

### Concepts you’re practicing
- File uploads (multipart form data)
- Storing files on disk (development-only approach)
- Validation (file type and size limits)
- Authorization (“only enrolled users can access the audio”)

### Allowed files
- `apps/api/chinese_practice/main.py`
- `apps/api/chinese_practice/storage.py` (you will create this)
- `apps/web/src/ui/PhraseCard.tsx` (extend your existing component)
- `apps/web/src/api/client.ts`

### Definition of Done
- Upload model audio and play it back from a phrase card.
- You can explain what “content-type validation” is and why we do it.

---

## Cursor prompts (copy/paste)

- “Explain what a multipart upload is and how FastAPI reads it.”
- “Create a small `store_upload()` helper that saves a file to disk and enforces max size.”
- “Show me how to return an audio file from FastAPI so `<audio>` can play it.”

---

## Tasks

1) Create `storage.py`
- Add a helper to save an uploaded file under a folder like `uploads/model_audio/...`.
- Validate:
  - content type starts with `audio/`
  - file size is limited (example: 20 MB)

2) Add API endpoints
- `POST /api/phrases/{phrase_id}/model-audio` (teacher uploads)
- `GET /api/phrases/{phrase_id}/model-audio` (enrolled users can play)

3) Update the UI
- In `PhraseCard`, add:
  - an `<audio controls>` player (when model audio exists)
  - a file input to upload model audio (teacher only)

---

## Verify
- Teacher uploads a small audio file and can play it.
- Student (enrolled) can play it.
- A non-enrolled user gets blocked (401 or 403).

---

## Explain-back questions
- What is “content type”?
- Why do we check it on the server (not just the UI)?
- Where is the authorization check for audio access?

