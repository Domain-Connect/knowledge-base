# Risks & Objections — DNS Provider

*Part of the [Domain Connect Knowledge Base](../00_MASTER.md) · Product Edition: DNS Providers*

---

## How to Use This Page

Every stakeholder you need on board will raise a different concern. This page groups the questions by who usually asks them, with a short answer you can use in the meeting and a pointer to the detail.

---

## From Your CEO

**"Is this a real standard, or a GoDaddy feature we'll end up abandoning?"**

It started at GoDaddy in 2016 and has run in production since. Today {{ facts.dns_providers }} DNS providers support it — including IONOS, Cloudflare, Squarespace Domains, WordPress.com and Plesk — and the IETF approved a dedicated working group (DCONN) in October 2025. The specification is a Standards Track working group draft. See [07 — Adoption & Ecosystem](../07_Adoption_and_Ecosystem.md).

**"What do we actually get for it?"**

Fewer support tickets on third-party DNS setup, more domains that get put into use — which renew at ~90% instead of ~70% — and an activation experience that matches the best in the market. See the [Business Case](./dns_01_business_case.md).

**"Does this make it easier for customers to use competitors' services instead of ours?"**

Customers connect to Microsoft 365 or Shopify whether or not you support Domain Connect; the only question is whether they succeed with you or struggle. A domain that is in use stays with you. And if you sell hosting, email or site-building products, the same protocol lets those products connect domains hosted *elsewhere* — you can be a service provider too.

---

## From Your CTO / Engineering Lead

**"How big is this?"**

A defined, one-time build: discovery endpoints, a consent flow on your existing login, a template engine and an internal template tool. The complex logic is available as an open-source reference library. The asynchronous OAuth flow is optional and can come later. See [Scope of Work](./dns_02_scope_of_work.md).

**"Will the spec change under us?"**

The protocol has been stable in production for a decade, and service providers depend on existing behaviour. The working group's job is to standardize and clarify what is deployed, through a public, consensus-driven process you can follow and participate in. Track it at the [IETF DCONN working group](https://datatracker.ietf.org/wg/dconn/about/).

**"Our zone write path isn't atomic / our platform is unusual."**

That is the main sizing driver, and worth a spike in Phase 0. The template engine needs to read current records and write a set of changes as one operation, so the user never ends up with half a configuration.

**"Do we have to integrate with every service provider?"**

No. Service providers integrate with the standard. You review and deploy their templates; most need no contact at all.

---

## From Your CISO / Security Team

**"We're letting third parties change our customers' DNS?"**

No third party can change anything on its own. Three controls must all pass:

1. **You approved the template** in advance. Requests for templates you have not deployed are rejected.
2. **The customer logs in with you** and you verify they own the domain.
3. **The customer approves** on a consent screen that you render and control.

The service provider can only supply values for the variables your approved template allows. See [08 — Security Model](../08_Security_Model.md).

**"What about phishing — someone tricking a user into pointing their domain at an attacker?"**

Service providers sign their requests with a key published in their own DNS; you verify the signature, so parameters cannot be tampered with in transit. Set a policy to require signing for templates that redirect web traffic (A, AAAA, CNAME). For unsigned templates with risky variables, the `warnPhishing` flag tells you to show an extra warning.

**"What is our vetting policy?"**

You decide. A practical starting point:

- Accept only templates merged into the public repository (already community-reviewed)
- Require signing (`syncPubKeyDomain`) for templates that affect where web traffic goes
- Prefer templates with narrowly scoped variables over ones where a variable is a full record value
- Re-review on every new template version
- Keep the ability to withdraw a template instantly

**"What doesn't it protect against?"**

A compromised service provider can still produce validly signed requests — which is why template vetting, not signing, is the primary trust boundary. Domain Connect also does not replace DNSSEC or protect a compromised DNS provider. These limits are documented openly in the specification.

---

## From Legal / Compliance

**"Who is liable if a template breaks a customer's setup?"**

The change is made by your system, at the customer's explicit request, after they have seen what will change. Conflicting records are identified and shown before approval. With template state tracking, a connected service can be disconnected cleanly. Review your terms of service to cover customer-approved changes initiated from a third-party site, and agree the consent-screen wording with legal.

**"Do we need contracts with service providers?"**

Not for synchronous-flow templates from the public repository — that is the point of the model. Some DNS providers choose to require terms for specific partners; that is your choice. The asynchronous (OAuth) flow involves a bilateral client registration with each partner.

---

## From Your Support Lead

**"Will this create new types of tickets?"**

Some — a customer abandoning the consent screen, a conflict they do not understand, a service whose template you have not deployed yet. These are fewer and simpler than manual-setup tickets: no transcription errors, deterministic results, and conflict detection that removes the "looks right but doesn't work" category. Ticket tagging from day one lets you prove the net effect.

**"What do we need to prepare?"**

A short playbook on the new flow, updated help articles for the services you support, and a tag for Domain Connect–related tickets.

---

## From Finance

**"What's the payback?"**

Build the estimate from your own ticket volumes and renewal data using the worksheet in the [Business Case](./dns_01_business_case.md). Present a conservative and an optimistic case, and propose a pilot on the top templates to replace assumptions with measured values.

**"What's the ongoing cost?"**

Mostly template review and catalogue management — a recurring process task, not an engineering team. See [Ongoing Operations](./dns_02_scope_of_work.md#ongoing-operations).

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Zone write path harder to integrate than expected | Medium | Schedule | Phase 0 spike; reuse reference library |
| Low consent completion due to UX friction | Medium | Value | Keep the screen short and plain-language; measure and iterate |
| Malicious or sloppy template deployed | Low | High | Vetting policy; signing required for traffic-steering templates; instant withdrawal |
| Service providers not showing the button for you | Low–Medium | Value | Get listed on domainconnect.org; contact allowlist-based service providers |
| Template backlog grows faster than reviews | Medium | Coverage | Prioritise by observed demand; lightweight review for low-risk records (e.g. TXT verification, DKIM) |
| Specification changes | Low | Rework | Follow the DCONN working group; changes go through public consensus |

---

*Previous: [Scope of Work](./dns_02_scope_of_work.md) · Next: [Executive Brief](./dns_04_executive_brief.md)*
