# 06 — Value by Audience

*Part of the [Domain Connect Knowledge Base](./00_MASTER.md)*

---

## Overview

Domain Connect creates value for every party involved in the domain lifecycle. The value is not abstract — it maps directly to measurable outcomes: support ticket reduction, renewal rate improvement, conversion rates, and reduced implementation cost. This document presents the value proposition as it should be communicated to each specific audience.

---

## For Domain Registries

Registries are in an unusual position: they benefit from Domain Connect without needing to implement it themselves. The value comes from higher utilization of their namespace.

### The core connection

CENTR renewal data shows a direct relationship between domain use and renewal:

- Domains with no content: ~70% renewal rate
- Domains with high content: ~90% renewal rate

Every additional domain that goes into active use is a domain that is 20 percentage points more likely to renew. DNS configuration friction is one of the primary barriers between registration and active use. Removing it has a direct, measurable impact on renewal revenue at the registry level.

### What registries can do

**Promote adoption among registrars.** The most effective lever a registry has is encouraging registrars and DNS providers in their ecosystem to implement Domain Connect. A registry can communicate the renewal rate data directly to its registrar base, framing Domain Connect implementation as a business-improvement initiative.

**Monitor namespace health.** Registries can look for `_domainconnect` TXT records in their zone data to understand what percentage of their registrars have implemented the protocol. This is a useful signal for namespace utilization quality.

**Support the IETF standardization.** The DCONN working group (approved October 2025) is the venue where the protocol's future is shaped. Registry participation ensures that TLD-operator concerns — DNSSEC bootstrapping, nameserver change flows, DS record automation — are addressed in the standard.

### Talking points for registries
- "Unused domains are renewal risk. DNS configuration failure is the most fixable part of the usage gap."
- "Domain Connect turns a 40-minute failure-prone process into a 30-second success. That's the difference between a domain in use and a non-renewed domain."
- "Every registrar in our ecosystem that implements Domain Connect increases the renewal quality of our zone."

---

## For DNS Providers and Registrars

This is the audience that implements Domain Connect and directly experiences the operational benefits. The value is immediate and concrete.

### Reduced support burden

DNS configuration is one of the leading sources of technical support tickets at registrars. Users who cannot configure their domains for Microsoft 365 or Google Workspace call support, open tickets, and sometimes churn. Domain Connect reduces this support load because:

- The process is automated — no manual record entry means no transcription errors
- The consent screen confirms what will happen in plain language — fewer "I didn't know what I was approving" situations
- Template-based application is deterministic — the same result every time

### Improved customer experience and retention

Customers who successfully connect their domains to their chosen services become invested users. The renewal rate data reflects this: connected domains with active services renew at dramatically higher rates than unused domains. A registrar that makes it easy to connect to services is a registrar that customers stay with.

### Competitive differentiation

A DNS provider that supports Domain Connect can offer one-click integration with 120+ service providers. A DNS provider that doesn't requires its customers to navigate manual DNS setup. In a market where most DNS functionality is commoditized, the user experience at domain activation is a genuine differentiator.

### "Implement once, benefit forever" scaling

The implementation investment is front-loaded: build the Domain Connect API endpoint once, implement the consent flow, deploy the template hosting infrastructure. After that, each new service provider is just a new template — no additional development. A single implementation connects you to the entire ecosystem of 120+ service providers.

### Talking points for DNS providers/registrars
- "We implemented Domain Connect once. Now our customers can connect to Microsoft 365, Google Workspace, Shopify, and 120+ other services in one click."
- "Support tickets for DNS configuration dropped significantly after we launched Domain Connect."
- "When our competitors' customers need help with DNS setup, they call support. When our customers do it, they click 'Connect'."

---

## For Service Providers

Service providers — the Shopifys, Microsofts, and Googles of the world — have an enormous stake in DNS configuration success. When customers can't configure their domain, the service itself cannot function. Conversion rates suffer. Customer satisfaction suffers.

### Fewer lost customers at the final step

The DNS configuration step is where ~50% of customers who have already registered a domain and signed up for a service abandon the process. These are motivated, paying customers who fail because the technical complexity is beyond them. Domain Connect eliminates this failure mode.

### Eliminated per-registrar support documentation

Without Domain Connect, Microsoft maintains 16 help sites for Microsoft 365 domain setup — 10 of them are registrar-specific, because every registrar's DNS interface is different. When a registrar updates its UI, Microsoft must update its documentation. When registrar documentation goes out of date, customers fail.

With Domain Connect, the service provider defines a template once. The DNS provider handles the UI. The service provider's documentation problem goes away.

### Faster, more reliable service activation

Template-based DNS configuration is deterministic. The same template, applied via Domain Connect, produces the same DNS records every time. There is no room for typos, field confusion, or missed steps. Service activation after DNS configuration succeeds at a near-100% rate compared to ~50% for manual configuration.

### Access to a growing ecosystem

Implementing Domain Connect means that any DNS provider who also implements it can offer one-click integration with your service — without any bilateral negotiation. Once your template is published, it can be adopted by all ~20 DNS providers in the ecosystem. New DNS providers that implement Domain Connect in the future automatically support your service.

### Talking points for service providers
- "DNS configuration is where we lose half our customers. Domain Connect is the fix."
- "We write one template. Every Domain Connect-compatible DNS provider can deploy it. No bilateral agreements, no custom integrations."
- "Our customers who go through Domain Connect activate their service successfully. Our customers who do manual DNS setup succeed about half the time."

---

## For End Users

End users are the ultimate beneficiaries of Domain Connect, and the value is the simplest to explain: it removes a technical burden that most people cannot handle.

### What users experience without Domain Connect

A small business owner who registers a domain and signs up for Microsoft 365 email must:

1. Log into their registrar's control panel
2. Find the DNS management section
3. Understand what MX, TXT, and CNAME records are
4. Read Microsoft's help documentation (which may be out of date for their specific registrar)
5. Create 7–15 individual DNS records, manually, one by one
6. Wait for DNS propagation
7. Troubleshoot when something doesn't work
8. About 50% of them give up before finishing

### What users experience with Domain Connect

1. Type their domain name into the service's interface
2. Click "Connect automatically" (or equivalent)
3. Log into their DNS provider (with their existing password)
4. See a plain-language description of what will be configured
5. Click "Connect"
6. Done

**Time:** Seconds, not 40+ minutes  
**Success rate:** Near 100%, not ~50%  
**DNS knowledge required:** None

### The informed consent angle

Domain Connect is not just about convenience — it is also about informed consent. The user sees exactly what DNS records will be changed, in plain language. They can cancel at any point. The DNS provider authenticates them independently. They retain control.

Compared to manual DNS entry, where users often blindly copy cryptic strings without understanding what they are doing, Domain Connect actually provides *more* transparency about what is happening to their domain.

---

## Value Map Summary

| Audience | Primary value | Measurable outcome |
|----------|--------------|-------------------|
| Registry | Higher namespace utilization → higher renewals | ~20 percentage point renewal rate improvement per active domain |
| DNS Provider / Registrar | Reduced support cost, improved retention, differentiation | Support ticket reduction; churn reduction |
| Service Provider | Higher service activation rate, eliminated per-registrar doc burden | Conversion from ~50% to ~100% at DNS config step |
| End User | No DNS knowledge required, seconds instead of 40 minutes | Near-100% success rate vs ~50% manual |

---

*Previous: [05 — Use Cases](./05_Use_Cases.md) | Next: [07 — Adoption & Ecosystem](./07_Adoption_and_Ecosystem.md)*
