# Quality bar (batteries included)

## Non-negotiables

- No secrets committed (session secrets, API keys).
- Validate inputs on the server.
- Enforce authorization on the API, not only in the UI.
- Prefer tests for permission rules.

## When adding endpoints

- Use clear request/response schemas.
- Return appropriate HTTP codes (401/403/404/400).
- Keep routes small; move logic into helper functions when needed.

## When adding UI features

- Handle loading + error states.
- Avoid duplicating API calls; keep them in a small `api/` module.

