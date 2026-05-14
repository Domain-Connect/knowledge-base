# 07 — Adoption and Ecosystem

*Part of the [Domain Connect Knowledge Base](./00_MASTER.md)*

---

## Current State (as of May 2026)

Domain Connect has crossed from experimental protocol to deployed infrastructure. The numbers reflect a mature ecosystem:

| Metric | Value |
|--------|-------|
| DNS Providers with Domain Connect support | ~20 |
| Share of .com zone covered by supporting providers | ~35% (May 2024) |
| Service Provider templates deployed | 720 |
| Service Providers with templates | 408 |
| GitHub contributors to template repository | 420 |
| Merged pull requests (template repository) | 831 |
| Years in production | 10 (first deployed ~2016) |

*Statistics from [stats.domainconnect.org](https://stats.domainconnect.org), generated 2026-05-14.*

35% of the .com zone is not a niche feature. It means that a service provider implementing Domain Connect can immediately offer one-click DNS setup to more than one in three .com domain owners.

---

## DNS Provider Implementations

The following DNS providers have deployed Domain Connect support. These are the companies that host authoritative DNS for user domains and have implemented the server-side API:

**Major implementations:**
- **GoDaddy** — the original proposer; one of the largest domain registrars globally
- **IONOS** — major European registrar and hosting provider
- **Cloudflare** — largest DNS resolver globally; significant DNS hosting footprint
- **Squarespace Domains** — inherited the former Google Domains customer base
- **WordPress.com** — major website hosting platform with integrated DNS
- **Plesk** — hosting control panel with DNS management used by thousands of hosters

Additional providers have implementations underway or deployed without public announcement.

The diversity of implementations matters: GoDaddy and IONOS together cover a very large share of consumer registrar customers. Cloudflare's implementation extends coverage to the technically sophisticated segment. WordPress.com and Squarespace Domains cover website-builder customers who are already motivated to connect their domain to a service.

---

## Service Provider Templates

The 720 templates from 408 service providers span the full range of online services. Notable implementations include:

**Email and productivity:**
- Microsoft Office 365 / Microsoft 365
- Google Workspace
- Apple iCloud+ (custom domain email)

**Website and e-commerce:**
- Shopify
- Squarespace
- Weebly

**Other services:**
- A wide range of SaaS platforms, email marketing services, and web application providers

The template registry is maintained publicly at [domainconnect.org](https://domainconnect.org) and on GitHub at [github.com/domain-connect](https://github.com/domain-connect).

---

## Standardization Timeline

### 2016 — First proposal
GoDaddy proposes Domain Connect at IETF 96 (REGEXT working group). The concept: a standardized protocol for automating DNS configuration at the point of service connection.

### 2016–2024 — Production deployment
Domain Connect is deployed in production by GoDaddy and other major DNS providers. The ecosystem grows organically. Templates accumulate. The protocol proves its approach in real-world conditions across hundreds of millions of domains.

### 2024 — IETF submission
The protocol specification is submitted to the IETF as an Internet-Draft (`draft-ietf-dconn-domainconnect`). This begins the formal standardization process.

### October 2025 — IETF working group approved
The IETF approves the formation of the DCONN (Domain Connect) working group. This is a significant milestone: it means the IETF has judged that the problem is real, the solution is worth standardizing, and there is sufficient community support to justify a dedicated working group.

### November 2025 — First working group meeting (IETF 124, Montreal)
The DCONN WG holds its inaugural meeting. The agenda covers the current draft, open issues, security considerations, and the adoption call. The WG formally adopts `draft-ietf-dconn-domainconnect-01` as a working group document.

### March 2026 — Draft version -01
`draft-ietf-dconn-domainconnect-01` is published, incorporating significant revisions based on working group feedback. Key additions include a detailed trust model section, clarified security considerations, and resolutions to issues raised at IETF 123.

---

## What IETF Standardization Means

For organizations that have been hesitant to implement Domain Connect because it appeared to be a vendor-led proprietary protocol, IETF standardization changes the calculus:

**It signals stability.** The protocol will not change arbitrarily. Changes go through the working group process, with public review and consensus requirements.

**It establishes a trust model.** The IETF review has forced explicit documentation of the trust model, security considerations, and known limitations — information that procurement and security teams need.

**It provides a reference point for procurement.** "We implement RFC X" is a statement that organizations with compliance requirements can point to. A working group draft in Standards Track status is on that path.

**It opens participation.** Any organization can participate in the DCONN working group — commenting on drafts, raising issues, proposing changes. This is the correct channel for shaping the protocol's future.

---

## The GitHub Repository and Open Source Ecosystem

Domain Connect is fully open source. All specification-related work is public:

- **Specification repository:** `github.com/domain-connect/spec`
- **Reference implementations:** Available for both DNS provider (server-side) and service provider (client-side) roles
- **Template registry:** Publicly browsable and submittable
- **Issue tracker:** Open for specification questions and implementation reports

The project also maintains a community LinkedIn page at `linkedin.com/company/domain-connect/` where implementers and practitioners connect.

---

## Adoption Trajectory and Outlook

The 35% .com zone coverage figure is a floor, not a ceiling. Several factors suggest continued growth:

**IETF standardization removes the biggest adoption blocker.** The most common reason cited by non-adopting DNS providers for not implementing was the perception that Domain Connect was a GoDaddy proprietary protocol. With IETF working group status, that objection is no longer available.

**Service provider pressure is growing.** Major SaaS platforms actively encourage their DNS provider partners to implement Domain Connect. As Microsoft, Google, and Shopify continue deploying Domain Connect as their preferred DNS configuration method, DNS providers face customer demand for support.

**The template network effect.** Each new DNS provider implementation makes 300+ existing templates immediately available to that provider's customers. Each new service provider template becomes available to all ~20 existing DNS provider implementations. The ecosystem's value grows with every participant.

**Extended use cases open new segments.** The DNSSEC bootstrapping and nameserver change use cases, if standardized in a future working group document, would draw in registry operators as direct participants — extending Domain Connect's reach beyond the registrar/service-provider axis.

---

*Previous: [06 — Value by Audience](./06_Value_by_Audience.md) | Next: [08 — Security Model](./08_Security_Model.md)*
