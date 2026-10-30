#!/usr/bin/env python3
"""QA check: no link in the generated site may return an HTTP error (404).

Starts a local HTTP server that publishes the site directory (default:
docs/) under the path of SITE_URL, like GitHub Pages publishes a project
site under /<repo>/, then crawls it: every HTML page is fetched over HTTP,
its href/src targets and <meta http-equiv="refresh"> redirects are resolved
against the page's real URL, and each target is requested. Crawling starts
at the site root and at every HTML file in the site directory, so pages that
nothing links to are checked as well.

With --url, no server is started and an already running site (e.g.
./serve.sh, or the published site) is crawled from that URL instead.

Links to other hosts, mailto:, tel:, javascript: and data: are not checked.

Usage:
    python3 .github/.scripts/check_links.py [SITE_DIR] [--site-url SITE_URL]
    python3 .github/.scripts/check_links.py --url http://localhost:8000/

Exit code is 1 if any broken link is found.
"""

import argparse
import functools
import re
import sys
import threading
import urllib.error
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote, urldefrag, urljoin, urlsplit

SKIP_SCHEMES = {"mailto", "tel", "javascript", "data"}
REFRESH_URL = re.compile(r"url\s*=\s*['\"]?([^'\"]+)", re.IGNORECASE)


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append(attrs[name])
        if tag == "meta" and (attrs.get("http-equiv") or "").lower() == "refresh":
            match = REFRESH_URL.search(attrs.get("content") or "")
            if match:
                self.links.append(match.group(1).strip())


class SiteHandler(SimpleHTTPRequestHandler):
    """Serves the site directory under base_path; anything else is a 404."""

    base_path = "/"

    def translate_path(self, path):
        url_path = urlsplit(path).path
        if not url_path.startswith(self.base_path):
            return str(Path(self.directory) / "\0outside-base-path")
        return super().translate_path("/" + url_path[len(self.base_path):])

    def log_message(self, format, *args):
        pass


class QuietServer(ThreadingHTTPServer):
    """fetch() closes non-HTML responses unread; ignore the resulting broken pipes."""

    def handle_error(self, request, client_address):
        if isinstance(sys.exc_info()[1], (BrokenPipeError, ConnectionResetError)):
            return
        super().handle_error(request, client_address)


def start_server(site_dir, base_path):
    handler = type("Handler", (SiteHandler,), {"base_path": base_path})
    server = QuietServer(
        ("127.0.0.1", 0), functools.partial(handler, directory=str(site_dir))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}{base_path}"


def fetch(url):
    """Return (status, final_url, html_or_None); redirects are followed."""
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            body = None
            if resp.headers.get_content_type() == "text/html":
                body = resp.read().decode("utf-8", errors="replace")
            return resp.status, resp.geturl(), body
    except urllib.error.HTTPError as err:
        return err.code, url, None
    except urllib.error.URLError as err:
        return f"error: {err.reason}", url, None


def seed_urls(site_dir, root_url):
    for html_file in sorted(site_dir.rglob("*.html")):
        rel = html_file.relative_to(site_dir).as_posix()
        if rel == "index.html" or rel.endswith("/index.html"):
            rel = rel[: -len("index.html")]
        yield root_url + quote(rel)


def crawl(root_url, seeds):
    origin = urlsplit(root_url)[:2]
    referrers = defaultdict(set)
    queue = [root_url, *seeds]
    seen = set(queue)
    broken = {}
    pages = 0
    while queue:
        url = queue.pop()
        status, final_url, body = fetch(url)
        if status != 200:
            broken[url] = status
            continue
        # Only crawl pages of this site; other paths on the host are just checked.
        if body is None or not final_url.startswith(root_url):
            continue
        pages += 1
        collector = LinkCollector()
        collector.feed(body)
        for link in collector.links:
            parts = urlsplit(link)
            if parts.scheme in SKIP_SCHEMES or (parts.scheme and parts.scheme not in ("http", "https")):
                continue
            target = urldefrag(urljoin(final_url, link)).url
            if urlsplit(target)[:2] != origin:
                continue
            referrers[target].add(final_url)
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return pages, len(seen), broken, referrers


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("site_dir", nargs="?", default="docs")
    parser.add_argument("--site-url", default="", help="URL the site was built for (its path is served)")
    parser.add_argument("--url", help="crawl an already running site instead of starting a server")
    args = parser.parse_args()

    if args.url:
        root_url = args.url.rstrip("/") + "/"
        seeds = []
    else:
        site_dir = Path(args.site_dir).resolve()
        if not site_dir.is_dir():
            sys.exit(f"Site directory not found: {site_dir}")
        path = urlsplit(args.site_url).path.strip("/")
        server, root_url = start_server(site_dir, f"/{path}/" if path else "/")
        seeds = list(seed_urls(site_dir, root_url))

    pages, checked, broken, referrers = crawl(root_url, seeds)
    print(f"Crawled {pages} pages and checked {checked} URLs under {root_url}")
    if broken:
        print(f"\n{len(broken)} broken URL(s):")
        for url, status in sorted(broken.items()):
            print(f"  {url} ({status})")
            for ref in sorted(referrers[url]):
                print(f"      linked from {ref}")
        sys.exit(1)
    print("No broken links.")


if __name__ == "__main__":
    main()
