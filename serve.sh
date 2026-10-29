#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-8000}
VENV=".venv"

if [ ! -d "$VENV" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -r requirements.txt
fi

.github/.scripts/build.sh "http://localhost:$PORT/" "$VENV/bin/mkdocs"

echo ""
echo "Serving at http://localhost:$PORT"
echo "  /                  landing"
echo "  /marketing-kb/     marketing edition"
echo "  /implementers-kb/  implementers edition"
echo "  /product-dns-kb/   product edition: DNS providers"
echo "  /product-sp-kb/    product edition: service providers"
echo ""
echo "Press Ctrl+C to stop."
cd docs && python3 -m http.server "$PORT"
