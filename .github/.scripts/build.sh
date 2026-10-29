#!/usr/bin/env bash
# Build the landing page and both editions into docs/, then check links.
#
# Usage: .github/.scripts/build.sh [BASE_URL] [MKDOCS]
#   BASE_URL  URL the docs/ tree is published at, e.g. the GitHub Pages URL
#             (default: http://localhost:8000/). Passed to MkDocs as SITE_URL,
#             so no deployment URL is hard-coded in the configs.
#   MKDOCS    mkdocs executable (default: mkdocs)
set -euo pipefail

BASE_URL=${1:-http://localhost:8000/}
BASE_URL="${BASE_URL%/}/"
MKDOCS=${2:-mkdocs}

echo "Building landing site..."
SITE_URL="$BASE_URL" "$MKDOCS" build --strict --config-file mkdocs.yml

echo "Building marketing site..."
SITE_URL="${BASE_URL}marketing-kb/" "$MKDOCS" build --strict --config-file mkdocs-marketing.yml

echo "Building implementers site..."
SITE_URL="${BASE_URL}implementers-kb/" "$MKDOCS" build --strict --config-file mkdocs-implementers.yml

echo "Checking links..."
python3 "$(dirname "$0")/check_links.py" docs --site-url "$BASE_URL"
