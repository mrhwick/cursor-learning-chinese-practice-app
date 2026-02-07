## Lesson 08: Classrooms + enrollment

### Goal
Make the app multi-user in a realistic way:
- a teacher creates a classroom
- students join via an invite code
- data is scoped to the classroom

### Concepts you’re practicing
- Relational data modeling (users, classrooms, enrollments)
- “Scope” (a phrase belongs to a classroom)
- Authorization based on membership (“are you enrolled?”)

### Allowed files
- `apps/api/chinese_practice/main.py`
- `apps/api/chinese_practice/models.py`
- `apps/api/chinese_practice/schemas.py`
- `apps/web/src/ui/App.tsx`

### Definition of Done
- Teacher can create a classroom and see an invite code.
- Student can join using the invite code.
- Phrases are visible only to enrolled users.

---

## Cursor prompts (copy/paste)

- “Propose the smallest DB schema for classrooms + enrollment. Explain each table.”
- “Show me the minimal endpoints needed for: create classroom, join classroom, list my classrooms.”
- “Where should we enforce membership checks, and how?”

---

## Tasks

1) Add tables
- `Classroom` (id, name, invite_code, owner_id)
- `Enrollment` (user_id, classroom_id)

2) Add endpoints
- `POST /api/classrooms` (teacher only) → returns classroom + invite code
- `POST /api/classrooms/join` (logged in) → joins by invite code
- `GET /api/classrooms` (logged in) → classrooms you’re enrolled in

3) Scope phrases
- Update your phrase model to include `classroom_id`.
- Update phrase endpoints to respect classroom membership.

4) Update the UI
- Teacher: create classroom and display invite code.
- Student: join classroom by invite code.
- Let the user pick an active classroom before showing phrases.

---

## Verify
- Teacher creates a classroom, copies invite code.
- Student joins with that invite code.
- Student can see phrases in that classroom.

---

## Explain-back questions
- What table represents membership?
- Why do we check enrollment before serving data?

