# 02 — What Is Domain Connect

*Part of the [Domain Connect Knowledge Base](./00_MASTER.md)*

---

## The One-Sentence Definition

**Domain Connect is an open-standard, application-level protocol that enables service providers to automatically configure the DNS records needed for their service on a user's domain — with the user's informed consent and without requiring any DNS knowledge.**

---

## The Formal Definition

From the IETF draft specification (draft-ietf-dconn-domainconnect-01):

> "Domain Connect offers a streamlined and automated solution. It empowers Service Providers to easily enable their services to work with user domains, simplifying both DNS provider discovery and DNS configuration. By abstracting away the complexities of manual DNS management through user-friendly web interactions, standard authentication, and template-based configurations, Domain Connect significantly improves the user experience."

---

## Origins and Status

- **Proposed by:** GoDaddy, 2016 (first presented at IETF 96, REGEXT working group)
- **Nature:** Open standard — freely available, no licensing fees, no vendor lock-in
- **Specification:** `draft-ietf-dconn-domainconnect-01` (IETF Standards Track)
- **Standardization:** IETF DCONN (Domain Connect) working group, approved October 2025; first meeting November 2025 (IETF 124, Montreal)
- **Authors:** Pawel Kowalik (DENIC), Arnold Blinn, Jon Kolker (GoDaddy), Sami Kerola (Cloudflare)

---

## What Domain Connect Is

- An **application-layer protocol** operating over HTTPS/REST
- A **standardized interface** between Service Providers and DNS Providers
- A **template-based system** where DNS configurations are pre-defined and pre-approved
- A **user consent flow** that puts the user in control while removing technical complexity
- A **discovery mechanism** so a service knows automatically whether a DNS provider supports the protocol
- **Both a synchronous flow** (one-time, user-present setup) and an **asynchronous OAuth flow** (for ongoing or multi-step DNS management)

---

## What Domain Connect Is NOT

Understanding the boundaries is important for accurate communication:

| Domain Connect is NOT... | Why this matters |
|--------------------------|-----------------|
| A DNS hosting service | It doesn't host DNS zones; it works with existing DNS providers |
| A domain registrar | It doesn't register domains; it configures DNS for already-registered domains |
| A replacement for DNS | It configures standard DNS records using the existing DNS system |
| A workaround or hack | It is a formal IETF standards-track protocol |
| An API for arbitrary DNS changes | Changes are strictly scoped to what the pre-approved template allows |
| Suitable for CI/CD automation pipelines | It is designed for user-driven consent flows, not headless automation |
| Suitable for private/enterprise DNS | It requires publicly accessible endpoints; private DNS requires extra work |

---

## The Three Actors

Domain Connect involves exactly three parties:

**Service Provider (SP)**

An entity offering a service that needs DNS configuration — e.g., Microsoft (Office 365), Google (Workspace), Shopify, Squarespace, Weebly, Apple (iCloud+). The SP knows what DNS records their service requires. They define this as a *template*. They cannot touch the user's DNS zone directly.

**DNS Provider (DNSP)**

An entity hosting the authoritative DNS zone for the user's domain. This is typically a registrar or a dedicated DNS hosting company — GoDaddy, IONOS, Cloudflare, WordPress.com, Squarespace Domains, Plesk, etc. The DNS Provider implements the Domain Connect protocol, vouches for the trustworthiness of templates, authenticates users, presents consent screens, and applies the DNS changes.

**User**

The domain owner who wants to connect their domain to a service. In the Domain Connect flow, the user:

- Enters their domain name at the service provider
- Is redirected to their DNS provider (automatically detected)
- Authenticates with their DNS provider (credentials they already have)
- Reviews and approves the changes in plain language
- Clicks "Connect"

The user never needs to understand what an A record, CNAME, MX record, or SPF TXT record is.

---

## The Core Innovation: Templates as a Contract

The central concept that makes Domain Connect work is the **template**. A template is a JSON-formatted file that:

1. **Identifies** the Service Provider and the specific service
2. **Defines** exactly which DNS records need to be created, modified, or deleted
3. **Specifies** which values are static and which are dynamic (variables filled in at runtime)
4. **Controls** how conflicts with existing DNS records should be handled
5. **Provides** metadata for the user consent screen (service name, logo, description)

Templates are exchanged between Service Providers and DNS Providers **out-of-band** — meaning the DNS Provider reviews, vets, and deploys each template manually. This vetting step is the foundation of the trust model: a DNS Provider only applies templates it has explicitly approved.

---

## The User Experience in Practice

**Before Domain Connect** (typical manual flow):

1. Sign up for a service → get told to "configure your DNS"
2. Navigate to separate registrar/DNS control panel
3. Find "DNS Management" or "Zone Editor"
4. Manually add 7–15 individual DNS records
5. Correctly interpret cryptic record types and values
6. Hope nothing was mistyped
7. Wait for propagation, troubleshoot if it doesn't work

**With Domain Connect:**

1. Enter domain name in the service provider interface
2. The service detects "GoDaddy supports Domain Connect for this service"
3. Click "Connect automatically"
4. Brief redirect to GoDaddy → sign in → click "Connect"
5. Done. DNS is configured. Confirmation shown immediately.

**Time:** Seconds, not 40 minutes  
**Success rate:** Near 100%, vs. ~50% manually  
**User knowledge required:** None

---

## Key Terminology

| Term | Definition |
|------|-----------|
| Template | A JSON file defining the DNS records a service needs, along with metadata and conflict-resolution rules |
| Service Provider (SP) | An entity offering a service requiring DNS configuration |
| DNS Provider (DNSP) | An entity hosting authoritative DNS zones, implementing the Domain Connect protocol |
| Synchronous Flow | A one-time, user-present DNS configuration flow |
| Asynchronous Flow | An OAuth-based flow enabling a service to make DNS changes over time with one-time user consent |
| `_domainconnect` record | A TXT/CNAME DNS record placed in a zone to advertise that the DNS provider supports Domain Connect |
| Discovery | The automated process by which a Service Provider detects whether a domain's DNS Provider supports Domain Connect |
| Template Application | The act of a DNS Provider writing the DNS records defined in a template to a user's zone |

---

*Previous: [01 — Problem & Context](./01_Problem_and_Context.md) | Next: [03 — How It Works](./03_How_It_Works.md)*
