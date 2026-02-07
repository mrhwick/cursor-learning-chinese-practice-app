# API (FastAPI)

## Setup (macOS)

From the repo root:

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
```

## Run

```bash
./run_dev.sh
```

Health check:
- `GET http://localhost:8000/api/health`

## Tests

```bash
./run_tests.sh
```

