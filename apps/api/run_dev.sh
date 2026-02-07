#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d ".venv" ]]; then
  echo "API venv not found. Create it with:"
  echo "  cd apps/api"
  echo "  python3 -m venv .venv"
  echo "  source .venv/bin/activate"
  echo "  python -m pip install -U pip"
  echo "  pip install -e \".[dev]\""
  exit 1
fi

source .venv/bin/activate

export API_SESSION_SECRET="${API_SESSION_SECRET:-dev-secret-change-me}"

exec uvicorn chinese_practice.main:app --host 0.0.0.0 --port 8000 --reload

