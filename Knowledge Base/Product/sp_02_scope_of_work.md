# Scope of Work — Service Provider

*Part of the [Domain Connect Knowledge Base](../00_MASTER.md) · Product Edition: Service Providers*

---

## The Short Version

Integrating Domain Connect as a service provider is a **small engineering build** plus an **ongoing partner-outreach effort**.

- **Build once:** a template describing your DNS records, request signing, a discovery check in your onboarding, a "Connect automatically" path with a return handler, and verification that the records are live.
- **Grow over time:** get your template deployed by the DNS providers your customers use. This is mostly relationship work, not engineering.

Start with the **synchronous flow**. It covers one-time setup with the customer present, it is the simplest to build, and every DNS provider in the ecosystem supports it. The asynchronous (OAuth) flow is an optional later phase for multi-step or ongoing DNS management.

---

## What You Build

| # | Component | What it does | Relative size | What makes it bigger |
|---|-----------|--------------|---------------|----------------------|
| 1 | **Template** | A JSON file listing the DNS records your service needs, with variables for per-customer values | Small | Several products or configurations (apex vs. subdomain, with/without email); records that vary a lot per customer |
| 2 | **Request signing** | Signs each redirect so its parameters cannot be tampered with; public key published in your DNS | Small | Strict key-management requirements (HSM/KMS, rotation policy) |
| 3 | **Discovery** | When a customer enters a domain: look up `_domainconnect`, fetch the DNS provider's settings, check whether your template is deployed | Small | High volume needing caching; many onboarding entry points |
| 4 | **Onboarding UX** | "Connect automatically" button, redirect or pop-up to the DNS provider, return handling, fallback to manual instructions | Small–Medium | Several onboarding flows, A/B testing, mobile apps |
| 5 | **Post-connect verification** | Confirm the records resolve, then activate the service | Small | Usually exists already for the manual path |
| 6 | **Observability** | Funnel per DNS provider: offered → clicked → returned → verified | Small | — |
| 7 | **Asynchronous flow** *(optional, later)* | OAuth client per DNS provider; apply or update templates without the customer present | Large | Each DNS provider is a separate bilateral setup |

Relative sizes are meant for ordering and planning conversations, not as estimates. Your engineering team should size each line against your own architecture.

!!! info "Reuse before you build"
    Open-source client libraries handle discovery, redirect construction and signing: [domainconnect_python](https://github.com/Domain-Connect/domainconnect_python) (Python) and [ext-domain-connect](https://github.com/gaalferov/ext-domain-connect) (PHP). A complete working service provider — with source — runs at [exampleservice.domainconnect.org](https://exampleservice.domainconnect.org/simple). For the template itself, start from an existing one for a similar service in the [template repository](https://github.com/Domain-Connect/Templates) and the patterns in [15 — Template Use Cases](../15_Template_Use_Cases.md).

---

## What You Do *Not* Build

- **No per-registrar integration.** One integration against the standard works with every supporting DNS provider.
- **No consent screen.** The DNS provider authenticates the customer and shows the consent screen.
- **No DNS write logic.** Conflict detection, SPF merging and the actual record changes are done by the DNS provider.
- **No access to customer credentials.** The customer logs in at their DNS provider, never with you.

---

## The Most Important Design Decision: A Stable Template

Every DNS provider reviews and deploys your template individually. A **new template version** means each of them has to review and redeploy it — so changing your template is slow and costly across the ecosystem.

Design for stability from day one:

- Point at **hostnames you control** (e.g. `%ACCOUNTID%.platform.yourcompany.com` via CNAME) rather than IP addresses that change with your infrastructure
- Use **`SPFM`** for SPF so your entry merges with other services' instead of overwriting them
- Keep **variables narrow** — only the part of a value that genuinely differs per customer
- Use **record groups** if customers need different subsets (for example website only, or website and email)
- Sign requests (`syncPubKeyDomain`) — DNS providers increasingly require it, and adding it later is a new version

Have someone who knows your DNS setup review the template with [11 — Template Reference](../11_Template_Reference.md) before you publish.

---

## Phased Plan

### Phase 0 — Discovery and decision

- Measure your addressable share with a `_domainconnect` lookup across a sample of customer domains (see [Business Case](./sp_01_business_case.md#size-the-opportunity-with-your-own-data))
- Baseline the domain-step funnel and DNS-related ticket volume
- Identify which template pattern fits your product ([15 — Template Use Cases](../15_Template_Use_Cases.md))
- Engineering spike with the example service and a client library

**Exit:** go/no-go decision with a sized plan and a target list of DNS providers.

### Phase 1 — Template and integration

- Write and test the template ([Online Editor](https://domainconnect.paulonet.eu/dc/free/templateedit), [linter](https://github.com/Domain-Connect/dc-template-linter))
- Generate keys, publish the public key in your DNS, implement signing
- Submit a pull request to the [template repository](https://github.com/Domain-Connect/Templates) and respond to community review
- Build discovery, the "Connect automatically" path, return handling and verification
- Keep the manual path as fallback everywhere

**Exit:** template merged in the repository; integration ready behind a feature flag.

### Phase 2 — DNS provider rollout

- Contact the DNS providers that matter most for your customer base, in order of share from Phase 0
- Turn on the button provider by provider as your template is deployed; measure each against the manual path
- Get listed on [domainconnect.org](https://www.domainconnect.org)

Plan for **days to weeks per DNS provider**: some deploy after a quick review, others have a more formal vetting process or ask for terms.

**Exit:** template live at your top DNS providers; KPIs measured against the manual baseline.

### Phase 3 — Optional extensions

- Asynchronous (OAuth) flow for multi-step setups (e.g. verify, then configure) or ongoing DNS changes
- Sell-and-configure partnership with a registrar

---

## Team and Roles

| Role | Involvement | Responsibilities |
|------|-------------|------------------|
| Product manager | Throughout | Business case, KPIs, DNS provider priority list, rollout decisions |
| Backend engineer(s) | Phase 1 | Signing, discovery, return handling, verification |
| Frontend / UX | Phase 1, then tuning | "Connect automatically" path, fallback, messaging |
| DNS-savvy engineer | Phase 0–1 | Template design and review, key publication |
| Security | Phase 1 | Key management, review of signing implementation |
| Partnerships / BD | Phase 2 onwards | Outreach to DNS providers, follow-up on deployment |
| Support / Docs | Phase 2 onwards | Simplified help content, ticket tagging |

---

## Ongoing Operations

| Activity | What it involves |
|----------|------------------|
| **DNS provider coverage** | Track which providers have deployed your template; follow up with the rest; deploy at new providers as they join |
| **Template lifecycle** | Avoid changes; when unavoidable, publish a new version and coordinate redeployment |
| **Key rotation** | Publish a new key under a new label; old and new keys can coexist during rollover |
| **Monitoring** | Funnel per DNS provider; alert on drops that indicate a provider-side issue |
| **Standards tracking** | Follow the IETF DCONN working group; optionally participate |

---

## Definition of Done for Launch

Engineering detail for each item is in [Getting Started: Service Provider](../13_Getting_Started_Service_Provider.md).

- [ ] Template reviewed for stability, tested in the Online Editor, linter clean
- [ ] Template merged in the public repository
- [ ] Signing key generated, stored securely, public key published in DNS
- [ ] Discovery and template-support check in every onboarding entry point
- [ ] "Connect automatically" path with return handling; manual fallback always available
- [ ] Records verified before the service is activated
- [ ] Template deployed by at least one DNS provider; end-to-end flow tested there
- [ ] Funnel metrics by DNS provider on a dashboard
- [ ] Support and help content updated

---

*Previous: [Business Case](./sp_01_business_case.md) · Next: [Risks & Objections](./sp_03_risks_and_objections.md)*
