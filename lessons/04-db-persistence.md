## Lesson 04: DB persistence (SQLite + migrations)

### Goal
Understand:
- what SQLite is
- what a migration is
- why we don’t store everything in memory

### Concepts you’re practicing
- A database is where the app stores data so it survives refresh/restart.
- A table is like a spreadsheet; rows are the individual items.
- A migration is a versioned change to the database structure.

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

---

## Cursor prompts (copy/paste)

- “I’m new to databases. Explain SQLite and migrations in simple terms.”
- “Propose the smallest steps to add SQLAlchemy + Alembic and create one table.”
- “Give me the exact terminal commands to initialize Alembic and generate a migration.”
- “After we add the DB, show me how `/api/phrases` queries the table.”

## Common stuck points

- “My migration didn’t run”: ask Cursor to help you verify the DB file exists and the migration ran.
- “Import errors”: ask Cursor to explain the error and propose the smallest fix.

