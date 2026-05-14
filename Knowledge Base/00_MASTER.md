# Domain Connect — Marketing Knowledge Base

**Version:** 1.0 | **Last updated:** May 2026  
**Author:** Pawel Kowalik, Head of Product Management, DENIC eG  
**Sources:** APNIC blog article (Oct 2025), ROW presentation (Oct 2025), IETF-124 DCONN WG presentation (Oct 2025), IETF draft-ietf-dconn-domainconnect-01 (Mar 2026), IETF 123 WG transcript

---

## About This Knowledge Base

This document is the master index for the Domain Connect marketing knowledge base. It is designed to serve as a comprehensive, authoritative source for:

- Social media posts (LinkedIn, X/Twitter)
- Blog articles (technical and non-technical)
- Conference presentations and talking points
- Partner and registrar outreach materials
- Press and analyst briefings

Each linked sub-document covers a specific angle in depth. This master document provides a concise overview and navigation guide.

---

## Quick Reference: What Is Domain Connect?

**Domain Connect** is an open-standard, application-level protocol that automates DNS configuration when a user connects a domain name to a third-party service (e.g., a website builder, email platform, or online store). It eliminates the need for users to manually create DNS records by enabling the service provider and the DNS provider to communicate directly — with the user simply giving informed consent.

- **Originally proposed by:** GoDaddy, 2016
- **Status:** Production-deployed; IETF standardization underway (DCONN working group, approved Oct 2025)
- **Specification:** draft-ietf-dconn-domainconnect-01 (Standards Track)

---

## Document Map

| # | Document | What it covers |
|---|----------|----------------|
| [01](./01_Problem_and_Context.md) | Problem & Context | Why DNS configuration is broken; domain growth & renewal data |
| [02](./02_What_Is_Domain_Connect.md) | What Is Domain Connect | Definition, scope, what it is not, key concepts |
| [03](./03_How_It_Works.md) | How It Works | Technical flows, templates, discovery, consent — explained accessibly |
| [04](./04_Protocol_Features.md) | Protocol Features Deep Dive | All protocol features with technical detail |
| [05](./05_Use_Cases.md) | Use Cases | Primary use cases, extended use cases, out-of-scope cases |
| [06](./06_Value_by_Audience.md) | Value by Audience | What Domain Connect means for each stakeholder group |
| [07](./07_Adoption_and_Ecosystem.md) | Adoption & Ecosystem | Current implementations, providers, standardization status |
| [08](./08_Security_Model.md) | Security Model | Trust model, security features, known considerations |
| [09](./09_Getting_Involved.md) | Getting Involved | How to implement, IETF participation, community resources |
| [10](./10_Key_Messages.md) | Key Messages & Soundbites | Ready-to-use messaging for social posts, blogs, press |
| [11](./11_Template_Reference.md) | Template Reference | Complete field-by-field reference for all template metadata and record flags |
| [12](./12_Getting_Started_DNS_Provider.md) | Getting Started: DNS Provider | Step-by-step implementation guide for DNS Providers |
| [13](./13_Getting_Started_Service_Provider.md) | Getting Started: Service Provider | Step-by-step integration guide for Service Providers |
| [14](./14_Storytelling.md) | Storytelling | First-person stories for DNS/SP CEOs, PMs, support, devs; user stories; plain-language explainers |
| [15](./15_Template_Use_Cases.md) | Template Use Cases | 9 use-case patterns from the template repository with examples, DNS setup guidance, and implementation notes |

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

## Navigation by Content Goal

**"Explain what Domain Connect is"** → [02](./02_What_Is_Domain_Connect.md), [03](./03_How_It_Works.md)

**"Make the business case"** → [01](./01_Problem_and_Context.md), [06](./06_Value_by_Audience.md)

**"Go deep on the technology"** → [03](./03_How_It_Works.md), [04](./04_Protocol_Features.md), [08](./08_Security_Model.md)

**"Find use cases"** → [05](./05_Use_Cases.md)

**"Write a LinkedIn post or blog intro"** → [10](./10_Key_Messages.md)

**"Convince a registrar or DNS provider"** → [06](./06_Value_by_Audience.md), [07](./07_Adoption_and_Ecosystem.md)

**"Answer 'Is it a real standard?'"** → [07](./07_Adoption_and_Ecosystem.md), [09](./09_Getting_Involved.md)

**"Build or review a template"** → [11](./11_Template_Reference.md), [15](./15_Template_Use_Cases.md)

**"Implement as a DNS Provider"** → [12](./12_Getting_Started_DNS_Provider.md)

**"Implement as a Service Provider"** → [13](./13_Getting_Started_Service_Provider.md), [15](./15_Template_Use_Cases.md)

**"Tell a story for a specific audience"** → [14](./14_Storytelling.md)
