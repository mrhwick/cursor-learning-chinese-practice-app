# Capstone spec: Chinese Practice Studio

## Summary

A small multi-user app for Chinese learners:
- students log in and practice phrases
- they hear **model audio**
- they submit **audio attempts** (upload or record)
- classmates/teacher leave **feedback** (comment + simple rubric)

## Roles

- **Teacher**
  - creates classrooms
  - invites students via invite code
  - creates phrases
  - uploads model audio
  - moderates feedback
- **Student**
  - joins a classroom
  - browses phrases
  - uploads/records submissions
  - leaves feedback

## MVP data model

- User (email, password_hash, role)
- Classroom (name, invite_code, owner_id)
- Enrollment (user_id, classroom_id)
- Phrase (classroom_id, chinese, pinyin, english, notes)
- ModelAudio (phrase_id, storage_path, content_type)
- Submission (phrase_id, user_id, storage_path, content_type)
- Feedback (submission_id, author_id, comment, score_tones, score_clarity)

## MVP screens (UI)

- Auth: signup/login/logout
- Classroom picker:
  - teacher: create classroom + see invite code
  - student: join via invite code
- Phrases:
  - list phrases
  - teacher: create phrase
  - per phrase: play model audio, upload model audio (teacher)
- Submissions:
  - per phrase: upload attempt, record attempt
  - list attempts with playback
- Feedback:
  - per submission: list feedback
  - leave feedback with rubric
  - delete feedback (author or classroom owner)

## Rubric (simple)

- Tones: 1–5
- Clarity: 1–5

## Stretch ideas

- Assignments + due dates
- Private submissions (teacher-only) vs public (class)
- Analytics (attempt count; improvement over time)
- Deployment + cloud storage for audio

