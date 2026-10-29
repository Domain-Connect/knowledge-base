# Domain Connect — Product Edition: DNS Providers

**Version:** 1.0 | **Last updated:** October 2026  
**Author:** Pawel Kowalik, Co-Author of Domain Connect specification  
**Sources:** {{ facts.src_ietf_draft }}, {{ facts.src_template_stats }}, {{ facts.src_support_stats }}, {{ facts.src_centr_renewal_study }}, {{ facts.src_row_2025 }}, {{ facts.src_centr_jamboree_2025 }}

---

## About This Edition

This edition is for **product managers at DNS providers and registrars** who need to decide whether to implement Domain Connect — and then convince their team, their engineering leads and their CEO.

It answers four questions in order:

1. **Why should we do this?** — the problem, the value, and how to size it for your business
2. **What exactly would we build?** — the components, phases, team and ongoing operations
3. **What could go wrong?** — security, liability, operational risk and the objections you will hear
4. **How do I get a yes?** — a 60-second pitch, a one-page executive brief and how to tailor the message per audience

You do not need to read the protocol specification to use this edition. Where technical depth helps a decision, the pages link to the relevant section.

Implementing it yourself or handing over to engineering? See the [Implementers Edition](../../implementers-kb/). Working on the Service Provider side? See the [Product Edition: Service Providers](../../product-sp-kb/).

---

## The One-Paragraph Summary

Your customers register domains to connect them to something — Microsoft 365, Google Workspace, Shopify, a website builder. Today that connection is a manual DNS task that about half of them fail, and the failure lands in your support queue and, eventually, in your renewal numbers: unused domains renew at ~70%, domains with real content at ~90%. Domain Connect lets the service provider hand the job to you: they publish a DNS template, you vet and deploy it, and your customer approves the change on your own consent screen in a few seconds. You build the capability once — discovery, a consent flow, a template engine — and gain access to **{{ facts.templates }} ready-made templates from {{ facts.service_providers }} service providers** without negotiating a single bilateral integration. {{ facts.dns_providers }} DNS providers, covering ~{{ facts.dc_share }} of scanned domains, already run it in production, and the protocol is on the IETF Standards Track.

---

## Reading Paths

| You have… | Read |
|-----------|------|
| **15 minutes** before a meeting | [Executive Brief](./Product/dns_04_executive_brief.md) |
| **One hour** to form your own opinion | [Business Case](./Product/dns_01_business_case.md) → [Scope of Work](./Product/dns_02_scope_of_work.md) → [Risks & Objections](./Product/dns_03_risks_and_objections.md) |
| **An afternoon** to prepare a proposal | All four product pages, then [How It Works](./03_How_It_Works.md), [Security Model](./08_Security_Model.md) and [Adoption & Ecosystem](./07_Adoption_and_Ecosystem.md) |
| **A hand-over to engineering** | [Getting Started: DNS Provider](./12_Getting_Started_DNS_Provider.md) and the [Implementers Edition](../../implementers-kb/) |

---

## Key Numbers for Your Slides

| Metric | Value |
|--------|-------|
| Templates ready to deploy | {{ facts.templates }} |
| Service providers with templates | {{ facts.service_providers }} |
| DNS providers live | {{ facts.dns_providers }} (incl. GoDaddy, IONOS, Cloudflare, Squarespace Domains, WordPress.com, Plesk) |
| Share of scanned domains on supporting DNS providers | ~{{ facts.dc_share }} ({{ facts.share_date }}) |
| Users who fail manual DNS setup (Microsoft 365) | ~50% |
| DNS records needed for Microsoft 365 | 7–15 |
| Renewal rate: no content vs high content | ~70% vs ~90% |
| In production since | 2016 |
| IETF DCONN working group approved | October 2025 |

*Ecosystem statistics from {{ facts.src_support_stats }} and {{ facts.src_template_stats }} ({{ facts.stats_date }}).*

---

## Document Map

| Document | What it gives you |
|----------|-------------------|
| [Business Case](./Product/dns_01_business_case.md) | Value levers, how to size the opportunity with your own data, KPIs |
| [Scope of Work](./Product/dns_02_scope_of_work.md) | Components, build-vs-reuse, phasing, team, ongoing operations |
| [Risks & Objections](./Product/dns_03_risks_and_objections.md) | Answers for your CTO, CISO, legal, support and finance |
| [Executive Brief](./Product/dns_04_executive_brief.md) | 60-second pitch, one-page brief, tailoring by audience, first steps after approval |
| [01 Problem & Context](./01_Problem_and_Context.md) | Domain growth decline, DNS failure rates, the three-actor gap |
| [02 What Is Domain Connect](./02_What_Is_Domain_Connect.md) | Definition, scope, what it is not |
| [03 How It Works](./03_How_It_Works.md) | Flows, templates, discovery, consent |
| [05 Use Cases](./05_Use_Cases.md) | What customers will connect, plus registrar-specific extended use cases |
| [06 Value by Audience](./06_Value_by_Audience.md) | Value for registries, DNS providers, service providers, users |
| [07 Adoption & Ecosystem](./07_Adoption_and_Ecosystem.md) | Who is live, standardization timeline |
| [08 Security Model](./08_Security_Model.md) | Trust model, signing, vetting — for your security review |
| [12 Getting Started: DNS Provider](./12_Getting_Started_DNS_Provider.md) | The step-by-step implementation guide your engineers will follow |
| [Stories](./14_Storytelling.md) | First-person stories from a DNS provider CEO, PM and support manager |
