# Domain Connect — Marketing & Communications Edition

**Version:** 1.0 | **Last updated:** May 2026  
**Author:** Pawel Kowalik, Co-Author of Domain Connect specification  
**Sources:** APNIC blog article (Oct 2025), ROW presentation (Oct 2025), IETF-124 DCONN WG presentation, IETF draft-ietf-dconn-domainconnect-01 (Mar 2026)

---

## About This Edition

This edition is for people who communicate Domain Connect to external audiences — partners, press, analysts, conference attendees, and social media followers. It focuses on the business case, key messages, and narrative tools.

| Who you are | What you'll find here |
|-------------|----------------------|
| **Marketing or communications professional** | Key messages, soundbites, blog openings, LinkedIn post templates, press angles |
| **Conference speaker or presenter** | Talking points, statistics, narrative flows, audience-specific stories |
| **Product manager or business lead** | Plain-language explainers, audience-specific value propositions |
| **Partner or registrar outreach** | Business case data, adoption statistics, ecosystem overview |

Looking for technical implementation details? See the [Implementers Edition](/implementers-kb/).

---

## The One-Paragraph Summary

Half of all users who try to connect their domain to a service like Microsoft 365 give up before finishing — because DNS configuration requires expert knowledge most people don't have. Domain Connect solves this with a standardized protocol: the service provider defines a DNS template, the DNS provider vouches for and hosts it, and the user simply clicks "Connect" and approves. What used to take 40 minutes of following instructions now takes seconds. With ~20 DNS providers already supporting it (covering 35% of the .com zone) and 720 templates from 408 service providers deployed, Domain Connect has crossed from experiment to infrastructure. IETF standardization — through the newly approved DCONN working group — is now locking it in as an internet standard.

---

## Core Statistics (as of May 2026)

| Metric | Value |
|--------|-------|
| DNS Providers supporting Domain Connect | ~20 |
| Share of .com zone covered | ~35% (May 2024) |
| Service Provider templates | 720 |
| Service Providers with templates | 408 |
| GitHub contributors to template repository | 420 |
| Merged pull requests (template repository) | 831 |
| Microsoft 365 DNS setup failure rate (without DC) | ~50% |
| MS 365 manual setup: DNS entries required | 7–15 |
| MS 365 manual setup: help sites maintained | 16 (10 registrar-specific) |
| MS 365 manual training time | 40 minutes |
| Domain renewal rate, no content | ~70% |
| Domain renewal rate, high content | ~90% |
| Year first proposed | 2016 (GoDaddy) |
| IETF WG approval | October 2025 |
| Statistics source | stats.domainconnect.org (2026-05-14) |

---

## Document Map

| # | Document | What it covers |
|---|----------|----------------|
| [01](./01_Problem_and_Context.md) | Problem & Context | Why DNS configuration is broken; domain growth & renewal data |
| [02](./02_What_Is_Domain_Connect.md) | What Is Domain Connect | Definition, scope, what it is not, key concepts |
| [03](./03_How_It_Works.md) | How It Works | Protocol flows explained accessibly — no prior DNS knowledge needed |
| [05](./05_Use_Cases.md) | Use Cases | Primary use cases with business context |
| [06](./06_Value_by_Audience.md) | Value by Audience | What Domain Connect means for registries, DNS providers, service providers, end users |
| [07](./07_Adoption_and_Ecosystem.md) | Adoption & Ecosystem | Current implementations, providers, standardization status |
| [08](./08_Security_Model.md) | Security Model | Trust model in plain language; how user consent works |
| [09](./09_Getting_Involved.md) | Getting Involved | Community, IETF participation, where to send partners |
| [10](./10_Key_Messages.md) | Key Messages & Soundbites | Ready-to-use messaging for social posts, blogs, press |
| [14](./14_Storytelling.md) | Storytelling | First-person stories for DNS/SP CEOs, PMs, support, devs; user stories; plain-language explainers |

---

## Navigation by Content Goal

**"Write a LinkedIn post or blog intro"** → [10 Key Messages](./10_Key_Messages.md)

**"Explain what Domain Connect is (non-technical)"** → [02 What Is](./02_What_Is_Domain_Connect.md), [03 How It Works](./03_How_It_Works.md)

**"Make the business case for a partner or registrar"** → [01 Problem & Context](./01_Problem_and_Context.md), [06 Value by Audience](./06_Value_by_Audience.md)

**"Find the right adoption numbers"** → [07 Adoption & Ecosystem](./07_Adoption_and_Ecosystem.md)

**"Prepare a conference talk"** → [10 Key Messages](./10_Key_Messages.md), [14 Storytelling](./14_Storytelling.md)

**"Answer 'Is it a real standard?'"** → [07 Adoption & Ecosystem](./07_Adoption_and_Ecosystem.md), [09 Getting Involved](./09_Getting_Involved.md)

**"Tell a story for a specific audience"** → [14 Storytelling](./14_Storytelling.md)

**"Explain it to someone with no technical background"** → [14 Storytelling — Explainers](./Stories/Explainers/explainers.md)
