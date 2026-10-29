# Executive Brief — DNS Provider

*Part of the [Domain Connect Knowledge Base](../00_MASTER.md) · Product Edition: DNS Providers*

---

## The 60-Second Pitch

> Our customers buy domains to connect them to Microsoft 365, Google Workspace, Shopify and hundreds of other services. Today that means typing DNS records by hand — and about half of them fail. Those failures become support tickets, and domains that never get used renew at ~70% instead of ~90%.
>
> Domain Connect is an open standard, in production since 2016 and now on the IETF Standards Track, that turns this into a one-click, customer-approved step on our own consent screen. {{ facts.dns_providers }} DNS providers — GoDaddy, IONOS, Cloudflare among them — already support it. We build it once, and {{ facts.templates }} ready-made templates from {{ facts.service_providers }} service providers become available to our customers without a single partner integration.
>
> I'm asking for a scoped Phase 1: the synchronous flow and our top templates, with a pilot to measure ticket deflection and activation before we scale.

---

## One-Page Brief

**Problem.** Connecting a domain to a third-party service requires manual DNS configuration. ~50% of users fail (Microsoft 365 data). Failed connections drive support load and leave domains unused; unused domains renew ~20 points lower than domains with content (CENTR 2024).

**Proposal.** Implement Domain Connect as a DNS provider: discovery endpoints, a consent flow on our existing login, a template engine, and a template review process.

**Why us, why now.**

- Service providers already check every domain for Domain Connect support; supporting it switches on their "Connect automatically" button for our customers
- The templates our customers need already exist and are community-reviewed
- IETF standardization (DCONN WG, Oct 2025) removes the "proprietary protocol" risk
- Domain growth is flat; retention is the growth lever

**Investment.** One-time build, front-loaded; reference library available for the complex logic. Ongoing cost is a template-review process, not a team. *[Insert engineering sizing from Phase 0.]*

**Expected outcomes.** *[Insert figures from the business-case worksheet.]*

- Fewer third-party DNS setup tickets for services we cover
- More domains with a connected service within 90 days of registration
- Higher renewal rate for connected domains

**Risks and controls.** Every change requires a template we approved, a customer logged in with us, and explicit approval on our consent screen. We require signed requests for templates that redirect web traffic.

**Decision requested.** Approve Phase 0 (sizing and vetting policy) and Phase 1 (synchronous flow and top templates), with a go/no-go on Phase 2 based on pilot KPIs.

---

## Tailoring the Message

| Audience | Lead with | Bring |
|----------|-----------|-------|
| **CEO** | Renewal and activation; competitive experience | The 60-second pitch, the numbers table, [DNS Provider CEO story](../Stories/dns_provider_ceo.md) |
| **Engineering** | Defined scope, reuse of the reference library, no per-partner work | [Scope of Work](./dns_02_scope_of_work.md), [Getting Started](../12_Getting_Started_DNS_Provider.md), [DNS Provider developer story](../Stories/dns_provider_dev.md) |
| **Security** | Three-control trust model; your vetting policy | [Security Model](../08_Security_Model.md), [Risks & Objections](./dns_03_risks_and_objections.md#from-your-ciso-security-team) |
| **Support** | Ticket deflection; simpler escalations | [DNS Provider support story](../Stories/dns_provider_support.md) |
| **Finance** | Worksheet with your own data; pilot before scale | [Business Case](./dns_01_business_case.md#size-the-opportunity-with-your-own-data) |

---

## Your First Steps After Approval

1. Run Phase 0: ticket analysis, zone scan, engineering spike, vetting policy
2. Join the community: [domainconnect.org/getting-started](https://www.domainconnect.org/getting-started/)
3. Hand engineering [Getting Started: DNS Provider](../12_Getting_Started_DNS_Provider.md) and the [Implementers Edition](../../../implementers-kb/)
4. Try the flow from the service-provider side at [exampleservice.domainconnect.org](https://exampleservice.domainconnect.org/simple) against an existing DNS provider, so the team sees the target experience
5. Set up the KPI dashboard before launch, so the baseline is measured

---

*Previous: [Risks & Objections](./dns_03_risks_and_objections.md) · Back to: [Product Edition overview](../00_MASTER.md)*
