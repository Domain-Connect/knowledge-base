# Risks & Objections — Service Provider

*Part of the [Domain Connect Knowledge Base](../00_MASTER.md) · Product Edition: Service Providers*

---

## How to Use This Page

Every stakeholder you need on board will raise a different concern. This page groups the questions by who usually asks them, with a short answer you can use in the meeting and a pointer to the detail.

---

## From Your CEO

**"Does this fix the problem for all our customers?"**

No — for the customers whose DNS provider supports Domain Connect and has deployed your template. Today {{ facts.dns_providers }} DNS providers, covering ~{{ facts.dc_share }} of scanned domains, support it. Measure your own share with a `_domainconnect` lookup on a sample of customer domains; it may be higher or lower than the .com figure depending on your market. The manual path stays for everyone else, so nobody is worse off.

**"Is this a real standard?"**

In production since 2016, supported by GoDaddy, IONOS, Cloudflare and others, used by {{ facts.service_providers }} service providers including Microsoft 365, Google Workspace and Shopify, and on the IETF Standards Track since the DCONN working group was approved in October 2025. See [07 — Adoption & Ecosystem](../07_Adoption_and_Ecosystem.md).

**"What's the payoff?"**

More customers through the domain step, faster, with fewer support tickets and less documentation to maintain. Size it with your own funnel data using the [Business Case](./sp_01_business_case.md) worksheet.

---

## From Your CTO / Engineering Lead

**"How big is this?"**

Small for the core synchronous integration: a template, request signing, a discovery check, a redirect and a return handler. Client libraries and a full example service exist. The asynchronous OAuth flow is the large item, and it is optional. See [Scope of Work](./sp_02_scope_of_work.md).

**"What if our infrastructure changes?"**

Template changes require every DNS provider to redeploy, so design the template to point at hostnames you control rather than IP addresses. That keeps infrastructure changes on your side, invisible to the template. See [A Stable Template](./sp_02_scope_of_work.md#the-most-important-design-decision-a-stable-template).

**"We need multi-step setup / ongoing DNS changes."**

That is the asynchronous (OAuth) flow. It works, but requires a bilateral client setup with each DNS provider and fewer providers support it. Most services start with the synchronous flow and add async only where needed.

---

## From Your CISO / Security Team

**"Are we handling customer DNS credentials?"**

No. The customer logs in at their own DNS provider. You never see their credentials or get general access to their zone.

**"What do we need to protect?"**

Your signing key. It proves to DNS providers that a request really comes from you. Store it like any other production signing secret and plan for rotation — new keys are published under a new label, so old and new can coexist.

**"Can an attacker abuse our template?"**

Signed requests cannot be altered in transit, and the DNS provider only applies templates it has reviewed, to a domain the logged-in customer owns, after explicit approval. Keep variables narrow so even a valid request can only produce the records your service legitimately needs. See [08 — Security Model](../08_Security_Model.md).

---

## From Design / UX

**"We don't control the consent screen."**

Correct — the DNS provider renders it, which is why customers trust it. Your service name and logo (from the template) are shown to the customer. You control everything before the redirect and after the return: set expectations ("You'll confirm at your domain provider"), offer pop-up or redirect, and handle the return cleanly.

**"What about customers whose provider doesn't support it?"**

They see your existing manual flow. Discovery tells you in advance which path to show, so customers never hit a dead end.

---

## From Partnerships / BD

**"Do we need contracts with every registrar?"**

Not for the synchronous flow. Your template goes through the public repository, and DNS providers deploy it under their own review. Some providers ask for terms or a contact before deploying, and the OAuth flow involves bilateral setup — but the default model has no per-partner contract.

**"How long until we're live at a given provider?"**

Plan for days to weeks per DNS provider after your template is merged. Start with the providers that hold most of your customers.

---

## From Your Support Lead

**"Will this create new types of tickets?"**

A few — a customer who abandons the consent screen, or a conflict with existing records that the DNS provider surfaces. These are rarer and easier than manual-setup tickets: the records are written exactly as specified, conflicts are shown before approval, and SPF is merged rather than overwritten. Tag tickets by path (Domain Connect vs. manual) from day one to show the difference.

---

## From Finance

**"What's the ongoing cost?"**

Mainly partner follow-up to expand DNS provider coverage, plus occasional key rotation. Engineering cost after launch is low as long as the template stays stable.

**"How do we know it worked?"**

The manual path remains for customers on non-supporting providers, which gives you a natural comparison group. Measure completion, time-to-verify and tickets by path.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Addressable share lower than expected for our customer base | Medium | Value | Measure in Phase 0 before committing; keep investment proportionate |
| Slow deployment of our template at key DNS providers | Medium | Schedule, value | Prioritise by customer share; engage early; get listed on domainconnect.org |
| Template needs to change after rollout | Medium | Rework across providers | Design for stability: hostnames over IPs, narrow variables, signing from day one |
| Template review requests revisions | Medium | Schedule | Start from a similar existing template; run the linter and Online Editor before submitting |
| Signing key compromised | Low | High | Secure key storage; rotation procedure; separate key labels |
| Consent drop-off at the DNS provider | Low–Medium | Value | Set expectations before redirect; measure completion per provider and share findings with them |

---

*Previous: [Scope of Work](./sp_02_scope_of_work.md) · Next: [Executive Brief](./sp_04_executive_brief.md)*
