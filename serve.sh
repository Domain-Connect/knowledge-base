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
# Like `python3 -m http.server`, but quiet when the browser drops a connection
# mid-transfer (cancelled prefetch / instant navigation), which is harmless.
cd docs && python3 - "$PORT" <<'EOF'
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class Server(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        if isinstance(sys.exc_info()[1], (BrokenPipeError, ConnectionResetError)):
            return
        super().handle_error(request, client_address)

try:
    Server(("", int(sys.argv[1])), SimpleHTTPRequestHandler).serve_forever()
except KeyboardInterrupt:
    pass
EOF
