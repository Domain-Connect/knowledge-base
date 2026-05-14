# Domain Connect — Implementers Edition

**Version:** 1.0 | **Last updated:** May 2026  
**Author:** Pawel Kowalik, Co-Author of Domain Connect specification  
**Sources:** IETF draft-ietf-dconn-domainconnect-01 (Mar 2026), IETF 123 WG transcript, IETF-124 DCONN WG presentation, Templates repository README

---

## About This Edition

This edition is for DNS providers, service providers, template authors, and protocol contributors. It focuses on the technical protocol, implementation guidance, and template authoring.

| Who you are | What you'll find here |
|-------------|----------------------|
| **DNS provider or registrar** implementing Domain Connect | Discovery endpoint, template hosting, OAuth flow, sync and async APIs |
| **Service provider** integrating Domain Connect | Template authoring, apply-template flow, signing, variable model |
| **Template author** | Field-by-field template reference, use-case patterns, contribution process |
| **Protocol contributor or IETF participant** | Full protocol specification context, security model, open issues, WG participation |

Looking for messaging, stories, or business-case materials? See the [Marketing & Communications Edition](../../marketing-kb/).

---

## Quick Reference: What Is Domain Connect?

**Domain Connect** is an open-standard, application-level protocol that automates DNS configuration when a user connects a domain name to a third-party service. The service provider defines a signed DNS template; the DNS provider hosts it and applies it upon user consent. The protocol supports both synchronous (redirect-based) and asynchronous (OAuth-based) flows.

- **Originally proposed by:** GoDaddy, 2016
- **Status:** Production-deployed; IETF standardization underway (DCONN working group, approved Oct 2025)
- **Specification:** draft-ietf-dconn-domainconnect-01 (Standards Track)
- **Template repository:** [github.com/Domain-Connect/Templates](https://github.com/Domain-Connect/Templates) — 720 templates, 408 service providers, 420 contributors

---

## Document Map

| # | Document | What it covers |
|---|----------|----------------|
| [02](./02_What_Is_Domain_Connect.md) | What Is Domain Connect | Definition, three-actor model, scope, what it is not |
| [03](./03_How_It_Works.md) | How It Works | Synchronous and async flows, template structure, discovery, consent |
| [04](./04_Protocol_Features.md) | Protocol Features Deep Dive | All protocol features with full technical detail |
| [05](./05_Use_Cases.md) | Use Cases | Primary, extended, and out-of-scope use cases |
| [06](./06_Value_by_Audience.md) | Value by Audience | Implementation benefits by stakeholder group |
| [08](./08_Security_Model.md) | Security Model | Trust model, URL signing, OAuth scoping, known considerations |
| [09](./09_Getting_Involved.md) | Getting Involved | IETF participation, GitHub contribution, community resources |
| [11](./11_Template_Reference.md) | Template Reference | Complete field-by-field reference for all template metadata and record flags |
| [12](./12_Getting_Started_DNS_Provider.md) | Getting Started: DNS Provider | Step-by-step implementation guide for DNS Providers |
| [13](./13_Getting_Started_Service_Provider.md) | Getting Started: Service Provider | Step-by-step integration guide for Service Providers |
| [15](./15_Template_Use_Cases.md) | Template Use Cases | 9 use-case patterns with examples, DNS setup guidance, and implementation notes |

---

## Use Case Detail Pages

| Use Case | Document |
|----------|----------|
| UC-01 Email Hosting | [Use Cases/UC-01_Email_Hosting.md](./Use Cases/UC-01_Email_Hosting.md) |
| UC-02 Email Authentication & Marketing | [Use Cases/UC-02_Email_Authentication_Marketing.md](./Use Cases/UC-02_Email_Authentication_Marketing.md) |
| UC-03 Email Security (DMARC) | [Use Cases/UC-03_Email_Security_DMARC.md](./Use Cases/UC-03_Email_Security_DMARC.md) |
| UC-04 Website Hosting (Apex) | [Use Cases/UC-04_Website_Hosting_Apex.md](./Use Cases/UC-04_Website_Hosting_Apex.md) |
| UC-05 Website Hosting (Subdomain) | [Use Cases/UC-05_Website_Hosting_Subdomain.md](./Use Cases/UC-05_Website_Hosting_Subdomain.md) |
| UC-05-2 Website Subdomain + SSL | [Use Cases/UC-05-2_Website_Subdomain_SSL.md](./Use Cases/UC-05-2_Website_Subdomain_SSL.md) |
| UC-06 CDN / WAF / Reverse Proxy | [Use Cases/UC-06_CDN_WAF_Reverse_Proxy.md](./Use Cases/UC-06_CDN_WAF_Reverse_Proxy.md) |
| UC-07 URL Redirect | [Use Cases/UC-07_URL_Redirect.md](./Use Cases/UC-07_URL_Redirect.md) |
| UC-08 Dynamic DNS | [Use Cases/UC-08_Dynamic_DNS.md](./Use Cases/UC-08_Dynamic_DNS.md) |
| UC-09 DNS Subdomain Delegation | [Use Cases/UC-09_DNS_Subdomain_Delegation.md](./Use Cases/UC-09_DNS_Subdomain_Delegation.md) |

---

## Navigation by Task

**"Implement Domain Connect as a DNS Provider"** → [12 Getting Started: DNS Provider](./12_Getting_Started_DNS_Provider.md)

**"Integrate Domain Connect as a Service Provider"** → [13 Getting Started: Service Provider](./13_Getting_Started_Service_Provider.md)

**"Build or review a template"** → [11 Template Reference](./11_Template_Reference.md), [15 Template Use Cases](./15_Template_Use_Cases.md)

**"Understand the full protocol"** → [03 How It Works](./03_How_It_Works.md), [04 Protocol Features](./04_Protocol_Features.md)

**"Understand the security model"** → [08 Security Model](./08_Security_Model.md)

**"Find a use-case pattern for my template"** → [15 Template Use Cases](./15_Template_Use_Cases.md)

**"Contribute to the IETF spec"** → [09 Getting Involved](./09_Getting_Involved.md)

**"Understand what the protocol does and doesn't cover"** → [02 What Is Domain Connect](./02_What_Is_Domain_Connect.md), [05 Use Cases](./05_Use_Cases.md)
