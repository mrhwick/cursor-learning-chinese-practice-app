# Using the reference implementation (without short-circuiting learning)

## The point

`reference/` is here so you can debug and learn from differences. It is **not** the primary path.

The reference implementation should be treated as **static** so the learner always has a stable “gold” to compare against.

## Rules of thumb

- **Try first**: attempt the lesson tasks before looking at `reference/`.
- **Compare small**: diff one file at a time.
- **Ask “why”**: when you see a difference, ask Cursor why that design might be better/worse.
- **Explain back**: after comparing, write 3 bullets in your own words explaining what you learned.

## Safe ways to use reference

- **After you pass tests**: compare structure/style decisions.
- **When you are stuck for >20 minutes**: compare only the failing area (one file).
- **To understand architecture**: read the high-level folder layout and route structure.

## What not to do

- Don’t copy/paste big chunks to “get it done.”
- Don’t open reference before you try—your brain won’t build the problem-solving muscles.

