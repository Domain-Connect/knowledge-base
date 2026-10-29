# Executive Brief — Service Provider

*Part of the [Domain Connect Knowledge Base](../00_MASTER.md) · Product Edition: Service Providers*

---

## The 60-Second Pitch

> The last step before our product delivers value is connecting the customer's domain — and it happens in a registrar control panel we don't control. About half of users fail manual DNS setup. That costs us activations, support time, and documentation we keep rewriting for every registrar.
>
> Domain Connect is an open standard, in production since 2016 and now on the IETF Standards Track, that replaces this step with a "Connect automatically" button. The customer approves at their DNS provider and comes back with DNS configured exactly right. GoDaddy, IONOS, Cloudflare and ~17 other DNS providers support it; Microsoft 365, Google Workspace and Shopify are among 408 services already using it.
>
> The integration is small, the manual path stays as fallback, and we can measure the lift directly. I'm asking for Phase 0 to measure our addressable share, then Phase 1 to build it and roll out at our top DNS providers.

---

## One-Page Brief

**Problem.** Connecting a domain requires customers to enter DNS records by hand at their registrar. ~50% fail (Microsoft 365 data). Failures cost activations, generate support tickets and require registrar-specific documentation that goes stale.

**Proposal.** Integrate Domain Connect: publish a template for our service, sign requests, detect support during onboarding and offer one-click setup where available.

**Why now.**

- {{ facts.dns_providers }} DNS providers, covering ~{{ facts.dc_share }} of scanned domains, already support it *[replace with our measured share]*
- {{ facts.service_providers }} service providers — including our peers — already have templates; customers increasingly expect one-click setup
- IETF standardization (DCONN WG, Oct 2025) means one integration with a long future
- The manual path stays, so risk is contained and the lift is measurable

**Investment.** Small engineering build for the synchronous flow, using open-source client libraries; partner effort to get the template deployed at key DNS providers. *[Insert engineering sizing from Phase 0.]*

**Expected outcomes.** *[Insert figures from the business-case worksheet.]*

- Higher completion of the domain step for customers on supporting providers
- Shorter time from signup to working domain
- Fewer DNS-related support tickets; less registrar-specific documentation

**Risks and controls.** Coverage is partial — measured up front, with manual fallback. Template changes are costly — designed for stability from day one. Signing key — stored and rotated like other production secrets. We never handle customer DNS credentials.

**Decision requested.** Approve Phase 0 (addressable share, baseline, sizing) and Phase 1 (template and integration), with Phase 2 rollout to DNS providers driven by measured results.

---

## Tailoring the Message

| Audience | Lead with | Bring |
|----------|-----------|-------|
| **CEO** | Activation and retention; peers already use it | The 60-second pitch, the numbers table, [Service Provider CEO story](../Stories/service_provider_ceo.md) |
| **Engineering** | Small, well-defined integration; libraries and example service | [Scope of Work](./sp_02_scope_of_work.md), [Getting Started](../13_Getting_Started_Service_Provider.md), [Service Provider developer story](../Stories/service_provider_dev.md) |
| **Security** | No customer credentials; signed requests; key management | [Security Model](../08_Security_Model.md), [Risks & Objections](./sp_03_risks_and_objections.md#from-your-ciso-security-team) |
| **Support** | Fewer "my email doesn't work" tickets; less documentation | [Service Provider support story](../Stories/service_provider_support.md) |
| **Product / growth team** | Funnel lift with a built-in comparison group | [Service Provider PM story](../Stories/service_provider_pm.md), [Business Case](./sp_01_business_case.md) |
| **Finance** | Worksheet with our own data; measure before scaling | [Business Case](./sp_01_business_case.md#size-the-opportunity-with-your-own-data) |

---

## Your First Steps After Approval

1. Run the `_domainconnect` lookup on a sample of customer domains to measure addressable share
2. Try the customer experience yourself at [exampleservice.domainconnect.org](https://exampleservice.domainconnect.org/simple) with a domain at a supporting DNS provider
3. Pick your template pattern in [15 — Template Use Cases](../15_Template_Use_Cases.md) and find a similar existing template in the [repository](https://github.com/Domain-Connect/Templates)
4. Hand engineering [Getting Started: Service Provider](../13_Getting_Started_Service_Provider.md) and the [Implementers Edition](../../../implementers-kb/)
5. Join the community at [domainconnect.org/getting-started](https://www.domainconnect.org/getting-started/) and start the conversation with your top DNS providers early

---

*Previous: [Risks & Objections](./sp_03_risks_and_objections.md) · Back to: [Product Edition overview](../00_MASTER.md)*
