# Domain Connect — Marketing Knowledge Base

A comprehensive knowledge base about the [Domain Connect](https://www.domainconnect.org) protocol, maintained by Pawel Kowalik, co-author of [draft-ietf-dconn-domainconnect-01](https://datatracker.ietf.org/doc/draft-ietf-dconn-domainconnect/).

## What is Domain Connect?

Domain Connect is an open standard that automates DNS configuration when a user connects a domain to a third-party service (website builder, email platform, online store, etc.). Instead of manually creating DNS records — a process that fails for ~50% of users — the service provider and DNS provider communicate directly, and the user simply gives informed consent.

- **Status:** Production-deployed since 2016; IETF Standards Track (DCONN WG, approved Oct 2025)
- **Scale:** ~20 DNS providers, 720 templates from 408 service providers, ~35% of the .com zone covered

## What this knowledge base is for

Source material for LinkedIn posts, blog articles, conference presentations, partner outreach, and analyst briefings — written from the perspective of a registry operator and protocol author.

## Knowledge Base

→ **[Start here: Master Index](./Knowledge%20Base/00_MASTER.md)**

| # | Document | What it covers |
|---|----------|----------------|
| [01](./Knowledge%20Base/01_Problem_and_Context.md) | Problem & Context | Why DNS configuration is broken; domain growth & renewal data |
| [02](./Knowledge%20Base/02_What_Is_Domain_Connect.md) | What Is Domain Connect | Definition, scope, what it is not, key concepts |
| [03](./Knowledge%20Base/03_How_It_Works.md) | How It Works | Technical flows, templates, discovery, consent |
| [04](./Knowledge%20Base/04_Protocol_Features.md) | Protocol Features | All protocol features with technical detail |
| [05](./Knowledge%20Base/05_Use_Cases.md) | Use Cases | Primary, extended, and out-of-scope use cases |
| [06](./Knowledge%20Base/06_Value_by_Audience.md) | Value by Audience | What Domain Connect means for each stakeholder group |
| [07](./Knowledge%20Base/07_Adoption_and_Ecosystem.md) | Adoption & Ecosystem | Current implementations, providers, standardization status |
| [08](./Knowledge%20Base/08_Security_Model.md) | Security Model | Trust model, URL signing, OAuth scoping |
| [09](./Knowledge%20Base/09_Getting_Involved.md) | Getting Involved | How to implement, IETF participation, community resources |
| [10](./Knowledge%20Base/10_Key_Messages.md) | Key Messages | Ready-to-use soundbites, LinkedIn posts, blog openings, pitches |
| [11](./Knowledge%20Base/11_Template_Reference.md) | Template Reference | Field-by-field reference for template metadata and record flags |
| [12](./Knowledge%20Base/12_Getting_Started_DNS_Provider.md) | Getting Started: DNS Provider | Step-by-step implementation guide for DNS Providers |
| [13](./Knowledge%20Base/13_Getting_Started_Service_Provider.md) | Getting Started: Service Provider | Step-by-step integration guide for Service Providers |
| [14](./Knowledge%20Base/14_Storytelling.md) | Storytelling | First-person stories and plain-language explainers by audience |
| [15](./Knowledge%20Base/15_Template_Use_Cases.md) | Template Use Cases | 8 use-case patterns with examples and implementation guidance |

## Structure

```
Knowledge Base/       — Markdown source (MkDocs docs_dir)
  Stories/            — story files per role/audience
    Explainers/       — plain-language explainers + index
  Use Cases/          — one file per template use-case pattern
Sources/              — raw source documents (do not modify)
  assets/             — logo files (PNG, EPS)
  Website/            — archived domainconnect.org pages
.github/workflows/
  pages.yml           — CI: build MkDocs and publish to GitHub Pages
mkdocs.yml            — MkDocs configuration
requirements.txt      — Python dependencies
```

## Website

The knowledge base is published as a static site using [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), styled to match the Domain Connect brand.

### Local development

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Deployment

Every push to `main` automatically builds and deploys the site to GitHub Pages via GitHub Actions. No manual steps required.

> **Repository setting:** Pages → Source must be set to **GitHub Actions**.

*Live stats: [stats.domainconnect.org](https://stats.domainconnect.org)*
