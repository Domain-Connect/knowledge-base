"""MkDocs hook: add a GoatCounter page-view counter to every page.

Injects the GoatCounter script into each page's <head>; it reports the
page path itself. Readers without JavaScript are counted through a
<noscript> image that requests COUNTER_URL with the page's path (edition
prefix included, e.g. /marketing-kb/03_How_It_Works/) as the p parameter.

Redirect-only pages (the edition index.md) are skipped so a visit is not
counted twice.
"""

import os
from urllib.parse import quote

COUNTER_URL = "https://dcss.dc.paulonet.eu/count"


def _prefix(config):
    root = os.path.join(os.path.dirname(config.config_file_path), "docs")
    rel = os.path.relpath(config.site_dir, root).replace(os.sep, "/")
    return "/" if rel == "." else f"/{rel}/"


def on_post_page(output, page, config):
    if 'http-equiv="refresh"' in (page.content or ""):
        return output
    path = quote(_prefix(config) + page.url, safe="/")
    snippet = (
        f'<script data-goatcounter="{COUNTER_URL}" async src="//gc.zgo.at/count.js"></script>\n'
        f'<noscript><img src="{COUNTER_URL}?p={path}" alt=""></noscript>'
    )
    return output.replace("</head>", f"{snippet}\n</head>", 1)
