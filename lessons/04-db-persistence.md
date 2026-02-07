## Lesson 04: DB persistence (SQLite + migrations)

### Goal
Understand:
- what SQLite is
- what a migration is
- why we don’t store everything in memory

### Allowed files
- `apps/api/pyproject.toml` (may need to add deps)
- `apps/api/chinese_practice/db.py` (you will create this)
- `apps/api/chinese_practice/models.py` (you will create this)
- `apps/api/alembic/*` (you will create this)
- `apps/api/chinese_practice/main.py`

### Definition of Done
- You can create one table in SQLite using a migration.
- You can add an endpoint that reads from the DB and returns JSON.

---

## Tasks

We are going to add persistence for the first time.

1) Add database dependencies to `apps/api/pyproject.toml` if needed (Cursor can help).
Suggested: `sqlalchemy`, `alembic`.

2) Create `db.py` and `models.py` with a single `Phrase` table.
Suggested fields:
- `id` (int, primary key)
- `chinese` (text)
- `pinyin` (text)
- `english` (text)

3) Initialize Alembic and create your first migration.

4) Add an endpoint:
- `GET /api/phrases` → returns a list of phrases from the DB.

Explain-back:
- What is the difference between “a table” and “a row”?
- What problem do migrations solve?

