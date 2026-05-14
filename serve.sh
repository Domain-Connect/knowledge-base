#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-8000}
VENV=".venv"

if [ ! -d "$VENV" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -r requirements.txt
fi

echo "Building landing site..."
"$VENV/bin/mkdocs" build --strict

echo "Building marketing site..."
"$VENV/bin/mkdocs" build --strict --config-file mkdocs-marketing.yml

echo "Building implementers site..."
"$VENV/bin/mkdocs" build --strict --config-file mkdocs-implementers.yml

echo ""
echo "Serving at http://localhost:$PORT"
echo "  /                  landing"
echo "  /marketing-kb/     marketing edition"
echo "  /implementers-kb/  implementers edition"
echo ""
echo "Press Ctrl+C to stop."
cd docs && python3 -m http.server "$PORT"
