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

export API_DATABASE_URL="sqlite+pysqlite:///:memory:"
export API_SESSION_SECRET="test-secret"
export API_UPLOAD_DIR="./.test_uploads"

rm -rf "$API_UPLOAD_DIR"
mkdir -p "$API_UPLOAD_DIR"

pytest -q

