# Domain Connect Knowledge Base

## Project purpose

This is a marketing knowledge base about the Domain Connect protocol. It serves as source material for LinkedIn posts, blog articles, conference presentations, partner outreach, and analyst briefings.

**Author:** Pawel Kowalik, Head of Product Management at DENIC eG — co-author of `draft-ietf-dconn-domainconnect-01`. DNS concepts do not need to be over-explained. Content should reflect the perspective of a registry operator and protocol author.

---

## Directory structure

```
Sources/                    — raw source documents (do not modify)
Knowledge Base/             — the knowledge base (14 linked Markdown documents)
  Stories/                  — individual story files (one per role/audience)
    Explainers/             — plain-language explainers (one per audience) + index
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

Statistics from [stats.domainconnect.org](https://stats.domainconnect.org) (updated 2026-05-14) unless noted otherwise:

- **720 templates** from **408 service providers** in the template repository
- **420 GitHub contributors**, **831 merged PRs** in the template repository
- **~20 DNS providers** support Domain Connect
- **~35% of the .com zone** covered by supporting DNS providers (May 2024)
- **~50%** of users fail manual DNS configuration (Microsoft 365 case study)
- Microsoft 365 requires **7–15 DNS records**, **16 help sites** (10 registrar-specific), **40 min** training
- Domain renewal rate: **~70%** (no content) vs **~90%** (high content) — CENTR 2024 study
- IETF DCONN working group approved **October 2025**
- Current specification: **draft-ietf-dconn-domainconnect-01** (March 2026)
- Live stats API: **https://stats.domainconnect.org/stats.json**

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
| Build or review a template | 11_Template_Reference.md |
| Implement as a DNS Provider | 12_Getting_Started_DNS_Provider.md |
| Implement as a Service Provider | 13_Getting_Started_Service_Provider.md |
| Tell a story for a specific audience | 14_Storytelling.md |

When updating statistics, fetch fresh data from `https://stats.domainconnect.org/stats.json` and update 00_MASTER.md, 07_Adoption_and_Ecosystem.md, 10_Key_Messages.md, and this file.
