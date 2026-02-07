#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

API_DIR="$ROOT_DIR/apps/api"
WEB_DIR="$ROOT_DIR/apps/web"

if [[ ! -d "$API_DIR" || ! -d "$WEB_DIR" ]]; then
  echo "Missing apps. Expected:"
  echo "  $API_DIR"
  echo "  $WEB_DIR"
  exit 1
fi

cleanup() {
  jobs -p | xargs -r kill || true
}
trap cleanup EXIT

echo "Starting API (http://localhost:8000) ..."
(cd "$API_DIR" && ./run_dev.sh) &

echo "Waiting for API to be ready..."
for i in $(seq 1 60); do
  if curl -fsS "http://localhost:8000/api/health" >/dev/null 2>&1; then
    echo "API is ready."
    break
  fi
  sleep 0.25
  if [[ "$i" == "60" ]]; then
    echo "API did not become ready in time. Check the API logs above."
    exit 1
  fi
done

echo "Starting Web (http://localhost:5173) ..."
(cd "$WEB_DIR" && ./run_dev.sh) &

wait

