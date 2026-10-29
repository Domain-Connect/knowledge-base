# Domain Connect — Product Edition: Service Providers

**Version:** 1.0 | **Last updated:** October 2026  
**Author:** Pawel Kowalik, Co-Author of Domain Connect specification  
**Sources:** {{ facts.src_ietf_draft }}, {{ facts.src_template_stats }}, {{ facts.src_support_stats }}, {{ facts.src_templates_readme }}, {{ facts.src_row_2025 }}, {{ facts.src_centr_jamboree_2025 }}

---

## About This Edition

This edition is for **product managers at service providers** — SaaS platforms, email and productivity suites, website builders, e-commerce platforms, marketing tools — anyone whose product asks customers to bring their own domain. It helps you decide whether to integrate Domain Connect and convince your team, your engineering leads and your CEO.

It answers four questions in order:

1. **Why should we do this?** — the problem, the value, and how to size it for your funnel
2. **What exactly would we build?** — the components, phases, team and ongoing operations
3. **What could go wrong?** — coverage, dependencies, security and the objections you will hear
4. **How do I get a yes?** — a 60-second pitch, a one-page executive brief and how to tailor the message per audience

You do not need to read the protocol specification to use this edition. Where technical depth helps a decision, the pages link to the relevant section.

Implementing it yourself or handing over to engineering? See the [Implementers Edition](../../implementers-kb/). Working on the DNS provider side? See the [Product Edition: DNS Providers](../../product-dns-kb/).

---

## The One-Paragraph Summary

Every time your onboarding says "now add these DNS records at your registrar", you lose customers — about half of users fail manual DNS setup, and the ones who make it often end up in your support queue with records entered wrong. Domain Connect lets you skip that step. You describe the records your service needs in a template, publish it once, and when a customer's DNS provider supports it, your onboarding shows a "Connect automatically" button: the customer logs in at their DNS provider, approves, and is sent back to you with DNS configured correctly. {{ facts.dns_providers }} DNS providers, including GoDaddy, IONOS and Cloudflare and covering ~{{ facts.dc_share }} of scanned domains, already support it, and **{{ facts.service_providers }} service providers** have already published templates. The protocol has been in production since 2016 and is on the IETF Standards Track.

---

## Reading Paths

| You have… | Read |
|-----------|------|
| **15 minutes** before a meeting | [Executive Brief](./Product/sp_04_executive_brief.md) |
| **One hour** to form your own opinion | [Business Case](./Product/sp_01_business_case.md) → [Scope of Work](./Product/sp_02_scope_of_work.md) → [Risks & Objections](./Product/sp_03_risks_and_objections.md) |
| **An afternoon** to prepare a proposal | All four product pages, then [How It Works](./03_How_It_Works.md), [Template Use Cases](./15_Template_Use_Cases.md) and [Adoption & Ecosystem](./07_Adoption_and_Ecosystem.md) |
| **A hand-over to engineering** | [Getting Started: Service Provider](./13_Getting_Started_Service_Provider.md) and the [Implementers Edition](../../implementers-kb/) |

---

## Key Numbers for Your Slides

| Metric | Value |
|--------|-------|
| Users who fail manual DNS setup (Microsoft 365) | ~50% |
| DNS records needed for Microsoft 365 | 7–15 |
| Help sites Microsoft maintains for this step | 16 (10 registrar-specific) |
| Support training needed for manual setup | 40 minutes |
| DNS providers live | {{ facts.dns_providers }} (incl. GoDaddy, IONOS, Cloudflare, Squarespace Domains, WordPress.com, Plesk) |
| Share of scanned domains on supporting DNS providers | ~{{ facts.dc_share }} ({{ facts.share_date }}) |
| Service providers with templates | {{ facts.service_providers }} ({{ facts.templates }} templates) |
| Notable service providers | Microsoft 365, Google Workspace, Apple iCloud+, Shopify, Squarespace |
| In production since | 2016 |
| IETF DCONN working group approved | October 2025 |

*Ecosystem statistics from {{ facts.src_support_stats }} and {{ facts.src_template_stats }} ({{ facts.stats_date }}).*

---

## Document Map

| Document | What it gives you |
|----------|-------------------|
| [Business Case](./Product/sp_01_business_case.md) | Value levers, how to size the opportunity with your own funnel data, KPIs |
| [Scope of Work](./Product/sp_02_scope_of_work.md) | Components, build-vs-reuse, phasing, team, ongoing operations |
| [Risks & Objections](./Product/sp_03_risks_and_objections.md) | Answers for your CTO, CISO, design, support and finance |
| [Executive Brief](./Product/sp_04_executive_brief.md) | 60-second pitch, one-page brief, tailoring by audience, first steps after approval |
| [01 Problem & Context](./01_Problem_and_Context.md) | DNS failure rates, the three-actor gap |
| [02 What Is Domain Connect](./02_What_Is_Domain_Connect.md) | Definition, scope, what it is not |
| [03 How It Works](./03_How_It_Works.md) | Flows, templates, discovery, consent |
| [05 Use Cases](./05_Use_Cases.md) | What services use it for, including multi-step flows |
| [06 Value by Audience](./06_Value_by_Audience.md) | Value for service providers, DNS providers, users |
| [07 Adoption & Ecosystem](./07_Adoption_and_Ecosystem.md) | Who is live, standardization timeline |
| [08 Security Model](./08_Security_Model.md) | Trust model, signing — for your security review |
| [13 Getting Started: Service Provider](./13_Getting_Started_Service_Provider.md) | The step-by-step integration guide your engineers will follow |
| [15 Template Use Cases](./15_Template_Use_Cases.md) | Which template pattern fits your product |
| [Stories](./14_Storytelling.md) | First-person stories from a service provider CEO, PM and support manager |
