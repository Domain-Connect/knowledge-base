# Template Use Cases

**Part of:** [Domain Connect Knowledge Base](./00_MASTER.md)  
**Audience:** Service providers building a Domain Connect template  
**Purpose:** Understand which use-case pattern fits your product, and how to implement it correctly

---

## Overview

The Domain Connect template repository contains 720+ templates from 408+ service providers. Analysing the full set reveals ten recurring DNS function patterns. Each pattern maps to a distinct type of SaaS product or service. This section documents each pattern with a concrete template example, implementation guidance, and things to watch out for.

Use this section when:
- You are a service provider deciding **which template structure** fits your product
- You want to see **real-world patterns** before writing your own template
- You need to understand **subtle rules** (conflict handling, groupIds, SPFM vs TXT) that trip up first-time implementers

---

## Use-Case Index

| # | Use Case | Typical records | Representative products |
|---|----------|----------------|------------------------|
| [UC-01](./Use%20Cases/UC-01_Email_Hosting.md) | **Email Hosting** | MX, SPFM, TXT (DKIM), CNAME (autodiscover) | Business email suites, hosted mailboxes |
| [UC-02](./Use%20Cases/UC-02_Email_Authentication_Marketing.md) | **Email Authentication & Marketing** | SPFM, TXT (DKIM), CNAME (return path, tracking) | Email marketing platforms, transactional email APIs |
| [UC-03](./Use%20Cases/UC-03_Email_Security_DMARC.md) | **Email Security & DMARC Management** | CNAME (_dmarc), SPFM, NS (_domainkey), CNAME (MTA-STS) | DMARC monitoring services, email security platforms |
| [UC-04](./Use%20Cases/UC-04_Website_Hosting_Apex.md) | **Website Hosting — Apex Domain** | A, AAAA, CNAME (www) | Website builders, e-commerce platforms, CMS hosting |
| [UC-05](./Use%20Cases/UC-05_Website_Hosting_Subdomain.md) | **Website Hosting — Subdomain / CNAME** | CNAME (subdomain) | SaaS custom domain features, app deployment platforms |
| [UC-05-2](./Use%20Cases/UC-05-2_Website_Subdomain_SSL.md) | **Website Hosting — Subdomain with SSL (DNS-01)** | CNAME (subdomain), TXT or CNAME (`_acme-challenge`) | Platforms issuing TLS certificates automatically on domain connection |
| [UC-06](./Use%20Cases/UC-06_CDN_WAF_Reverse_Proxy.md) | **CDN, WAF & Reverse Proxy** | A (WAF IP), CNAME (www → @), CNAME (proxy) | Web application firewalls, CDN edge networks, reverse proxies |
| [UC-07](./Use%20Cases/UC-07_URL_Redirect.md) | **URL Redirect** | A, AAAA (redirect service IPs) | URL shorteners, domain redirect services |
| [UC-08](./Use%20Cases/UC-08_Dynamic_DNS.md) | **Dynamic DNS** | A, AAAA (low TTL, client-updated) | DDNS clients, home server connectivity, IoT devices |
| [UC-09](./Use%20Cases/UC-09_DNS_Subdomain_Delegation.md) | **DNS Subdomain Delegation** | NS (subdomain) | Protocol overlay services, managed sub-zone hosting |

---

## How to Use This Section

1. **Identify your pattern** — find the use case that matches what your service does with DNS.
2. **Read the full page** — each page explains the DNS mechanics, the value to end users, and implementation specifics.
3. **Adapt the example template** — the example uses fictional names under `.example` TLD; replace with your own `providerId` and real values.
4. **Cross-reference** — see [11_Template_Reference.md](./11_Template_Reference.md) for full field documentation and [13_Getting_Started_Service_Provider.md](./13_Getting_Started_Service_Provider.md) for the submission process.

---

## Common Patterns Across All Use Cases

Regardless of use case, every well-constructed template shares these properties:

- **`syncPubKeyDomain`** is set to the domain hosting your `domainconnect.json` discovery record — required for the synchronous flow
- **`syncRedirectDomain`** lists all OAuth redirect origins your application uses
- **`groupId`** groups logically related records so DNS providers can apply or skip them as a unit
- **`ttl`** is set to `3600` for stable records; use `60`–`600` only for records that change frequently (e.g. dynamic DNS)
- **Variables** use `%variableName%` syntax; names are case-sensitive and must match exactly between template and your service's API call

---

*See also: [11_Template_Reference.md](./11_Template_Reference.md) · [13_Getting_Started_Service_Provider.md](./13_Getting_Started_Service_Provider.md)*
