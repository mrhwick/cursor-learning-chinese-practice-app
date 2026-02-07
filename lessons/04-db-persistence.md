## Lesson 04: DB persistence (SQLite + migrations)

### Goal
Understand:
- what SQLite is
- what a migration is
- why we don’t store everything in memory

### Allowed files
- `apps/api/alembic/versions/*`
- `apps/api/chinese_practice/models.py`
- `apps/api/chinese_practice/db.py`

### Definition of Done
- You can explain what a migration does
- You can point to where tables are defined

---

## Tasks

1) Find the migration file in `apps/api/alembic/versions/` and explain what tables it creates.\n
2) Ask Cursor:\n
- “If I wanted to add a `difficulty` field to phrases, what changes would I make (models + migration + API + UI)?”\n
You don’t need to implement it yet—just explain the steps.

