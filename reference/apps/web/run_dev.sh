#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d "node_modules" ]]; then
  echo "node_modules not found. Install deps with:"
  echo "  cd apps/web"
  echo "  npm install"
  exit 1
fi

exec npm run dev

