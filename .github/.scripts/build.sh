#!/usr/bin/env bash
# Build the landing page and all editions into docs/, then check links.
#
# Usage: .github/.scripts/build.sh [BASE_URL] [MKDOCS]
#   BASE_URL  URL the docs/ tree is published at, e.g. the GitHub Pages URL
#             (default: http://localhost:8000/). Passed to MkDocs as SITE_URL,
#             so no deployment URL is hard-coded in the configs.
#   MKDOCS    mkdocs executable (default: mkdocs)
#
# Refreshes data/facts.yml from the statistics sources first (update_facts.py).
# If they cannot be reached, the committed data/facts.yml is used. Set
# SKIP_FACTS_UPDATE=1 to build with the committed file without fetching.
set -euo pipefail

BASE_URL=${1:-http://localhost:8000/}
BASE_URL="${BASE_URL%/}/"
MKDOCS=${2:-mkdocs}

if [ "${SKIP_FACTS_UPDATE:-}" != "1" ]; then
  echo "Updating facts..."
  python3 "$(dirname "$0")/update_facts.py" ||
    echo "WARNING: facts update failed; building with the committed data/facts.yml" >&2
fi

echo "Building landing site..."
SITE_URL="$BASE_URL" "$MKDOCS" build --strict --config-file mkdocs.yml

echo "Building marketing site..."
SITE_URL="${BASE_URL}marketing-kb/" "$MKDOCS" build --strict --config-file mkdocs-marketing.yml

echo "Building implementers site..."
SITE_URL="${BASE_URL}implementers-kb/" "$MKDOCS" build --strict --config-file mkdocs-implementers.yml

echo "Building product (DNS provider) site..."
SITE_URL="${BASE_URL}product-dns-kb/" "$MKDOCS" build --strict --config-file mkdocs-product-dns.yml

echo "Building product (service provider) site..."
SITE_URL="${BASE_URL}product-sp-kb/" "$MKDOCS" build --strict --config-file mkdocs-product-sp.yml

echo "Checking links..."
python3 "$(dirname "$0")/check_links.py" docs --site-url "$BASE_URL"
