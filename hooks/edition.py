"""MkDocs hook: point shared edition-chooser links at the edition's own overview.

Both editions build from the same docs_dir, so pages link to 00_MASTER.md
(the edition chooser) and index.md redirects to it. Inside an edition that
sends readers to a chooser page whose links are relative to the site root.
Configure the edition overview in the MkDocs config:

    extra:
      edition_overview: 00_MASTER_marketing.md

and this hook rewrites the index.md redirect and every Markdown link to
00_MASTER.md to target that page instead.
"""

import posixpath
import re

MASTER = "00_MASTER.md"
MD_LINK = re.compile(r"(\]\()([^)\s#]*00_MASTER\.md)(#[^)\s]*)?(\))")
REFRESH = re.compile(r'(http-equiv="refresh"\s+content="0;\s*url=)00_MASTER/(")')


def on_page_markdown(markdown, page, config, files):
    overview = config.extra.get("edition_overview")
    if not overview:
        return markdown
    src = page.file.src_uri
    page_dir = posixpath.dirname(src)

    if src == "index.md":
        target = overview[: -len(".md")] + "/"
        return REFRESH.sub(rf"\g<1>{target}\g<2>", markdown)

    def rewrite(match):
        resolved = posixpath.normpath(posixpath.join(page_dir, match.group(2)))
        if resolved != MASTER:
            return match.group(0)
        rel = posixpath.relpath(overview, page_dir or ".")
        return f"{match.group(1)}{rel}{match.group(3) or ''}{match.group(4)}"

    return MD_LINK.sub(rewrite, markdown)
