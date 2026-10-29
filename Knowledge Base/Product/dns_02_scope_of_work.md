# Scope of Work — DNS Provider

*Part of the [Domain Connect Knowledge Base](../00_MASTER.md) · Product Edition: DNS Providers*

---

## The Short Version

Implementing Domain Connect as a DNS provider is a **front-loaded, one-time build** followed by a **light, ongoing operational process**.

- **Build once:** discovery endpoints, a browser-based consent flow on top of your existing login, a template engine that writes records into your zones, and an internal tool to manage templates.
- **Operate continuously:** review and deploy templates from service providers, monitor the flow, and keep the catalogue in line with what your customers use.

After the build, each additional service provider is a **template review and a deployment decision** — not a development project.

Start with the **synchronous flow**. It covers one-time setups with the customer present — the overwhelming majority of real-world use — and every service provider in the ecosystem supports it. The asynchronous (OAuth) flow is an optional later phase.

---

## What You Build

| # | Component | What it does | Relative size | What makes it bigger |
|---|-----------|--------------|---------------|----------------------|
| 1 | **Discovery** | Answers `_domainconnect.<domain>` TXT queries for hosted zones; serves a JSON settings document; answers "is template X deployed?" | Small | DNS platform cannot synthesize the TXT answer without per-zone records; multiple brands or platforms |
| 2 | **Consent flow (sync UX)** | Receives the redirect from the service provider, authenticates the user with your existing login, checks they own the domain, shows what will change, applies on approval, redirects back | Medium | Multiple login systems, reseller/white-label brands, localisation, accessibility requirements |
| 3 | **Template engine** | Resolves variables, detects conflicts with existing records, merges SPF, applies record groups, writes all changes atomically | Medium–Large | Zone write API that is not atomic; unusual record storage; no reuse of the reference library |
| 4 | **Signature verification** | Fetches the service provider's public key from DNS and verifies signed requests | Small | — |
| 5 | **Template management** | Stores deployed templates, imports from the public repository, supports review/approve/rollback and versions | Small–Medium | Formal change-management requirements |
| 6 | **Template state tracking** *(recommended)* | Records which template wrote which records, enabling clean disconnect/revert and accurate cross-service conflict handling | Medium | Exposing "connected services" to customers in the control panel |
| 7 | **Observability** | Funnel metrics (requests → logins → consents → applies), errors per template and per service provider, abuse signals | Small | — |
| 8 | **Asynchronous flow** *(optional, later)* | OAuth 2.0 authorization, template-scoped tokens, API for service providers to apply/remove templates without the user present | Large | Per-partner OAuth client onboarding; no existing OAuth server |

Relative sizes are meant for ordering and planning conversations, not as estimates. Your engineering team should size each line against your own architecture.

!!! info "Reuse before you build"
    The hardest logic — variable resolution, conflict detection, SPF merging — is available as an open-source Python library, [DomainConnectApplyZone](https://github.com/domain-connect/DomainConnectApplyZone). It takes the current zone, a template and the variables, and returns the changes to apply. Your team handles reading and writing the zone. Even if you do not use Python, it is a precise executable reference to port from. If your platform runs on a hosting control panel that already ships Domain Connect (for example Plesk), check what you get out of the box first.

---

## What You Do *Not* Build

It is as important to tell your team what is out of scope:

- **No per-partner integrations.** Service providers integrate against the standard, not against you.
- **No templates.** Service providers write and maintain their own; you review them.
- **No new identity system.** Customers log in with the credentials they already have.
- **No changes at the registry.** Domain Connect operates on the DNS zones you host.
- **No general-purpose DNS API for third parties.** Changes are limited to what a template you approved allows, on a domain the customer authorised.

---

## Integration Points in Your Platform

These are the existing systems the work touches. Getting the owners of these systems into the room early is the best way to de-risk the estimate.

| System | Why it is touched |
|--------|-------------------|
| Authoritative DNS platform | Answer `_domainconnect` TXT queries for hosted zones |
| Customer identity / login (incl. SSO, 2FA) | Authenticate the user during the consent flow |
| Account and domain ownership data | Verify the user controls the domain in the request |
| Zone management / DNS API | Read current records, write the new ones atomically |
| Control panel front end | Consent screen styling; optionally a "connected services" view |
| Web edge / WAF | Public endpoints for discovery and the consent flow |
| Analytics / data warehouse | Funnel and KPI tracking |

---

## Phased Plan

### Phase 0 — Discovery and decision

- Pull the support-ticket and zone-scan data described in the [Business Case](./dns_01_business_case.md)
- Pick the first templates (usually Microsoft 365 and Google Workspace, plus the top services found in your zones)
- Engineering spike against the integration points above; read [Getting Started: DNS Provider](../12_Getting_Started_DNS_Provider.md)
- Agree the template vetting policy with security (see [Risks & Objections](./dns_03_risks_and_objections.md))

**Exit:** go/no-go decision with a sized plan.

### Phase 1 — Minimum viable launch (synchronous flow)

- Components 1–5 and 7 from the table above
- Pass the test templates provided by the project: `exampleservice.domainconnect.org` template 1 (unsigned) and template 2 (signed)
- Deploy the first production templates
- Train support on the new flow; update help content
- Get listed on [domainconnect.org](https://www.domainconnect.org)

**Exit:** real customers connecting real services; funnel metrics flowing.

### Phase 2 — Scale the catalogue and the experience

- Template state tracking and a "connected services" view with disconnect
- Work through the backlog of templates by observed demand
- Contact service providers that maintain an allowlist of DNS providers so they enable you in their flow
- Tune the consent screen based on completion data

**Exit:** most observed service demand covered; support deflection measurable.

### Phase 3 — Optional extensions

- Asynchronous (OAuth) flow for service providers that need multi-step or ongoing DNS management
- Strategic flows: sell-and-configure partnerships, your own products acting as a service provider

---

## Team and Roles

| Role | Involvement | Responsibilities |
|------|-------------|------------------|
| Product manager | Throughout | Business case, template priorities, KPIs, partner outreach |
| Backend engineers | Phases 1–2 | Discovery, template engine, zone integration, template management |
| Frontend / UX | Phase 1, then tuning | Consent screen, redirects, control-panel integration |
| DNS / platform engineer | Phase 1 | `_domainconnect` TXT answers on the authoritative platform |
| Security | Phase 0–1, then per template | Vetting policy, signature requirements, review of the consent flow |
| Support lead | Phase 1 onwards | Playbooks, ticket tagging, feedback loop |
| Legal / compliance | Phase 0 | Terms covering third-party initiated changes, consent wording |
| Marketing / partnerships | Launch onwards | Launch announcement, listing, service-provider relationships |

---

## Ongoing Operations

The run cost is mostly **process**, not engineering:

| Activity | What it involves |
|----------|------------------|
| **Template review** | New templates and new versions of existing ones arrive through the public repository. Review against your vetting policy, deploy or reject. The repository's own community review catches most quality issues before you see them. |
| **Catalogue management** | Track which services your customers use and close gaps; retire templates for discontinued services. |
| **Partner contact** | Some service providers want to be told you are live; OAuth partners need client credentials. |
| **Monitoring** | Watch error rates per template and per service provider; investigate unusual apply patterns. |
| **Standards tracking** | Follow the IETF DCONN working group for specification changes; optionally participate. |

---

## Definition of Done for Launch

Use this as the acceptance checklist for Phase 1. Engineering detail for each item is in [Getting Started: DNS Provider](../12_Getting_Started_DNS_Provider.md).

- [ ] `_domainconnect` answered for all hosted zones
- [ ] Settings and template-query endpoints live
- [ ] Consent flow: login → ownership check → consent screen → apply → redirect
- [ ] Signed requests verified; unsigned requests rejected for templates that require signing
- [ ] Conflict detection and SPF merging working
- [ ] Both project test templates pass end-to-end
- [ ] First production templates reviewed under the agreed policy and deployed
- [ ] Support trained, help content updated, ticket tags in place
- [ ] Funnel metrics on a dashboard
- [ ] Listed on domainconnect.org

---

*Previous: [Business Case](./dns_01_business_case.md) · Next: [Risks & Objections](./dns_03_risks_and_objections.md)*
