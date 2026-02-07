## Lesson 09: Audio upload + playback (model audio)

### Goal
Teacher uploads a model audio clip for a phrase; students can play it.

### Allowed files
- `apps/api/chinese_practice/main.py`
- `apps/api/chinese_practice/storage.py` (you will create this)
- `apps/web/src/ui/PhraseCard.tsx` (extend your existing component)
- `apps/web/src/api/client.ts`

### Definition of Done
- Upload model audio and play it back from a phrase card.
- You can explain what “content-type validation” is and why we do it.

---

## Tasks

1) Add server-side file storage
- Create `apps/api/chinese_practice/storage.py` with a helper that saves an uploaded file to disk.
- Validate:
  - content type starts with `audio/`
  - file size is limited (pick a number like 20 MB)

2) Add API endpoints
- `POST /api/phrases/{phrase_id}/model-audio` (teacher uploads)
- `GET /api/phrases/{phrase_id}/model-audio` (enrolled users can play)

3) Add UI
- Add an `<audio controls>` player to the phrase card.
- Add an “Upload model audio” file input for teachers only.

