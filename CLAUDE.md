# Domain Connect Knowledge Base

## Project purpose

This is a knowledge base about the Domain Connect protocol. It serves as source material for implementation work (DNS providers, service providers), protocol contribution and IETF participation, communications and marketing (LinkedIn posts, blog articles, press briefings), and conference presentations and partner outreach.

**Author:** Pawel Kowalik — co-author of `draft-ietf-dconn-domainconnect-01`. DNS concepts do not need to be over-explained. Content should reflect the perspective of a registry operator and protocol author.

---

## Directory structure

```
Sources/                    — raw source documents (do not modify)
  assets/                   — logo files (PNG, EPS)
  Website/                  — archived domainconnect.org pages (reference for style/colors)
Knowledge Base/             — the knowledge base (MkDocs docs_dir)
  Stories/                  — individual story files (one per role/audience)
    Explainers/             — plain-language explainers (one per audience) + index
  Use Cases/                — one document per template use-case pattern
  Product/                  — product-manager pages (business case, scope, risks, exec brief) for DNS providers (dns_*) and service providers (sp_*)
  assets/                   — logo and favicon for the website (copied from Sources/assets)
  stylesheets/              — custom CSS (extra.css) with DC brand colors and Open Sans font
  index.md                  — root redirect to Overview (do not remove)
docs/                       — MkDocs build output (git-ignored; published via GitHub Actions)
.github/workflows/
  pages.yml                 — GitHub Actions workflow: build MkDocs, check links, deploy to GitHub Pages
  check-links.yml           — GitHub Actions workflow: build MkDocs and check links on PRs and non-main pushes
.github/.scripts/
  build.sh                  — builds all five sites into docs/ for a given base URL, then runs check_links.py
  check_links.py            — QA: fails if any internal link in the built docs/ would 404
  update_facts.py           — refreshes data/facts.yml from the statistics sources
data/
  facts.yml                 — generated ecosystem numbers behind the {{ facts.<key> }} placeholders (do not edit by hand)
  sources.yml               — hand-maintained titles and URLs of cited sources ({{ facts.src_<key> }} placeholders)
hooks/
  edition.py                — MkDocs hook: points index.md redirect and 00_MASTER.md links at the edition overview
  facts.py                  — MkDocs hook: replaces {{ facts.<key> }} placeholders with values from data/facts.yml and data/sources.yml
mkdocs.yml                  — MkDocs configuration
requirements.txt            — Python dependencies (mkdocs, mkdocs-material)
.venv/                      — local Python virtual environment (git-ignored)
CLAUDE.md                   — this file
```

### Knowledge Base documents

| File | Content |
|------|---------|
| 00_MASTER.md | Master index, statistics table, navigation guide |
| 01_Problem_and_Context.md | Domain growth decline, DNS configuration failure rates |
| 02_What_Is_Domain_Connect.md | Definition, scope, what it is and isn't, three actors |
| 03_How_It_Works.md | Synchronous and async flows, template structure, discovery |
| 04_Protocol_Features.md | All protocol features with technical detail |
| 05_Use_Cases.md | Primary, extended, and out-of-scope use cases |
| 06_Value_by_Audience.md | Value for registries, DNS providers, service providers, end users |
| 07_Adoption_and_Ecosystem.md | Deployment numbers, standardization timeline |
| 08_Security_Model.md | Trust model, URL signing, OAuth scoping, security considerations |
| 09_Getting_Involved.md | Implementation guides, IETF participation, community resources |
| 10_Key_Messages.md | Ready-to-use soundbites, post templates, blog openings, pitches |
| 11_Template_Reference.md | Exhaustive field-by-field reference for all template metadata and record flags, with usage stats |
| 12_Getting_Started_DNS_Provider.md | Step-by-step implementation guide for DNS Providers |
| 13_Getting_Started_Service_Provider.md | Step-by-step integration guide for Service Providers |
| 14_Storytelling.md | Index of stories and explainers; Stories/ subfolder contains individual files per role/audience |
| 15_Template_Use_Cases.md | Index of 8 use-case patterns; Use Cases/ subfolder has one document per pattern with examples and implementation guidance |
| 00_MASTER_product_dns.md / 00_MASTER_product_sp.md | Overviews of the two Product editions (reading paths, key numbers, document map) |
| Product/dns_01–04, Product/sp_01–04 | Business case (with sizing worksheet and KPIs), scope of work, risks & objections, executive brief (pitch + one-page brief) — for DNS provider and service provider PMs respectively |

### Source documents

| File | Description |
|------|-------------|
| `DC_APNIC blog_2025_Claude_long.md` | APNIC blog article, Oct 2025 |
| `DomainConnect-ROW-2025v2.pdf` | Registration Operations Workshop presentation, Oct 2025 |
| `IETF-124-domain-connect_v4.pdf` | IETF 124 DCONN WG presentation |
| `draft-ietf-dconn-domainconnect-01.txt` | IETF Standards Track draft, Mar 2026 |
| `ietf 123 transcript.txt` | IETF 123 DCONN WG session transcript |
| `DomainConnect-CENTR-Jamboree-2025.pdf` | CENTR Jamboree 2025 presentation |
| `Templates-README.md` | Domain-Connect/Templates repository README — contribution process and quality rules |

---

## Key facts

Ecosystem numbers are **not hard-coded** in content pages. They live in `data/facts.yml` and are referenced as `{{ facts.<key> }}` placeholders, resolved at build time by `hooks/facts.py` (an unknown key fails the build). Current values (2026-10-29) — check `data/facts.yml` for the latest:

- **2,207 templates** (`templates`) from **1,436 service providers** (`service_providers`) — DNS provider support data
- **455 GitHub contributors** (`contributors`), **2,136 merged PRs** (`merged_prs`) in the template repository
- **294 DNS providers** (`dns_providers`, supporting at least one template) support Domain Connect, running on **22 software stacks** (`dns_provider_stacks`)
- **~42% of scanned domains** (`dc_share`; 80.0M of 190.6M domains, September 2026) are on supporting DNS providers
- **~50%** of users fail manual DNS configuration (Microsoft 365 case study)
- Microsoft 365 requires **7–15 DNS records**, **16 help sites** (10 registrar-specific), **40 min** training
- Domain renewal rate: **~70%** (no content) vs **~90%** (high content) — CENTR 2024 study
- IETF DCONN working group approved **October 2025**
- Current specification: **draft-ietf-dconn-domainconnect-01** (March 2026)
- Sources of `data/facts.yml`: DNS provider support data from [pawel-kow/DomainConnectSupportStatsData](https://github.com/pawel-kow/DomainConnectSupportStatsData) (`statsdata/providers/`), published at [Domain Connect Support Stats](https://pawel-kow.github.io/DomainConnectSupportStats/) (Beta); template repository data (contributors, PRs, field and record type usage) from **https://stats.domainconnect.org/stats.json**

The other figures (failure rate, Microsoft 365 numbers, renewal rates, IETF dates) are static research facts and stay as plain text in content pages.

---

## Content generation guidance

| Goal | Start here |
|------|-----------|
| Write a LinkedIn post or blog intro | 10_Key_Messages.md |
| Explain what Domain Connect is | 02, 03 |
| Make the business case | 01, 06 |
| Go deep on technology | 03, 04, 08 |
| Find use cases | 05 |
| Convince a registrar or DNS provider | 06, 07 |
| Answer "Is it a real standard?" | 07, 09 |
| Build or review a template | 11_Template_Reference.md, 15_Template_Use_Cases.md |
| Implement as a DNS Provider | 12_Getting_Started_DNS_Provider.md |
| Implement as a Service Provider | 13_Getting_Started_Service_Provider.md |
| Tell a story for a specific audience | 14_Storytelling.md |
| Help a PM decide and pitch internally | Product/dns_* or Product/sp_* |

When writing a number that comes from the statistics sources, use a `{{ facts.<key> }}` placeholder (keys: see `data/facts.yml`; `*_plus` keys give rounded prose values such as "2,200+"). To refresh the numbers, run `python3 .github/.scripts/update_facts.py` (`--source DIR` reads a local checkout of the data repository, `--check` only reports whether the file is out of date) and commit `data/facts.yml`; to add a key, extend that script. `build.sh` runs the update before every build, so deployed sites always use fresh data; if the sources cannot be reached it falls back to the committed file (`SKIP_FACTS_UPDATE=1` skips the fetch). Also update the current values in this file.

When listing or citing sources, link them through `data/sources.yml`: `{{ facts.src_<key> }}` renders `[title](url) (date, note)` (no link when the source has no public URL), so don't repeat the date in the page; `src_<key>_url`, `src_<key>_title` and `src_<key>_date` give the parts. Add new sources there rather than writing the URL into a page, so a moved source is fixed in one place.

---

## Website / MkDocs

The knowledge base is published as a static website using [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

**Brand colors** (from domainconnect.org Ascension theme):
- Primary: `#03263B` · Secondary: `#0b3954` · Accent: `#00bfff` · Tertiary: `#bddae6`
- Font: Open Sans 300/400/700 (Google Fonts)

There is a landing page (`mkdocs.yml`, from `Root/`) plus four editions, each with its own MkDocs config:

| Config | Audience | Output |
|--------|----------|--------|
| `mkdocs-marketing.yml` | Marketing, comms, speakers | `docs/marketing-kb/` |
| `mkdocs-implementers.yml` | DNS/service providers, protocol contributors | `docs/implementers-kb/` |
| `mkdocs-product-dns.yml` | Product managers at DNS providers / registrars | `docs/product-dns-kb/` |
| `mkdocs-product-sp.yml` | Product managers at service providers | `docs/product-sp-kb/` |

**Local development:**
```bash
python3 -m venv .venv          # first time only
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve --config-file mkdocs-marketing.yml     # http://127.0.0.1:8000
.venv/bin/mkdocs serve --config-file mkdocs-implementers.yml  # http://127.0.0.1:8000
```

**Build:**
```bash
.venv/bin/mkdocs build --strict --config-file mkdocs-marketing.yml
.venv/bin/mkdocs build --strict --config-file mkdocs-implementers.yml
```
Same pattern for `mkdocs-product-dns.yml` and `mkdocs-product-sp.yml`. Output goes to the edition's `docs/<edition>/` directory (git-ignored on `main`).

**Full build + link check** (what CI runs):
```bash
.github/.scripts/build.sh [BASE_URL] [.venv/bin/mkdocs]   # BASE_URL defaults to http://localhost:8000/
```
Refreshes `data/facts.yml` (see Key facts), builds all five configs with `SITE_URL` set per site, then serves `docs/` on a temporary local HTTP server, crawls every page and fails with a list of every URL that returns an error, with the pages linking to it. To crawl an already running site instead: `python3 .github/.scripts/check_links.py --url http://localhost:8000/`. Runs in CI on every PR and push (`check-links.yml`) and before deploy (`pages.yml`, with the URL from `actions/configure-pages`).

**Edition links:** all editions share `Knowledge Base/`, so `index.md` and links to `00_MASTER.md` are rewritten per build by `hooks/edition.py` to the edition's overview (`extra.edition_overview` in each config). Keep linking to `./00_MASTER.md` in content pages. **Site URL:** no deployment URL is stored in the repo. Each config reads `site_url: !ENV SITE_URL`; `build.sh` sets it (base URL, `+marketing-kb/`, `+implementers-kb/`, `+product-dns-kb/`, `+product-sp-kb/`), and a plain `mkdocs build`/`serve` leaves it unset. It mainly matters for `404.html`, whose links MkDocs renders as absolute URLs.

**Deployment:** Every push to `main` triggers `.github/workflows/pages.yml`, which builds all sites and deploys the entire `docs/` tree to GitHub Pages. In the repository settings, Pages source must be set to **GitHub Actions**.

**Do not commit the `docs/` directory** — it is regenerated by CI on every deploy.
