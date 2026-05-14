# Domain Connect Explained — For an IT Department Member

*Part of the [Domain Connect Storytelling](../../14_Storytelling.md) collection · [Explainers index](./explainers.md)*

---

Domain Connect is a standardized protocol for delegated DNS record management, operating on a consent-based, template-scoped model. If you've worked with OAuth, the mental model translates directly.

**The core model:**

A Service Provider (SP) — Microsoft 365, Google Workspace, a SaaS platform — defines the DNS records their service requires in a JSON template. That template is vetted by the DNS Provider (DNSP) — the registrar or DNS host holding the zone — before any record modification is permitted. The end user approves the specific operation at runtime through a consent screen presented by the DNSP, under the DNSP's authentication context.

No DNS record is modified without three conditions being met: the SP's template has been pre-approved by the DNSP, the user is authenticated to the DNSP, and the user has explicitly consented to the specific record changes for the specific domain.

**The synchronous flow in brief:**

1. SP performs DNS discovery: `_domainconnect.<domain>` TXT → settings document → template availability check
2. SP constructs a redirect URL with template ID, domain, variable values, and an RS256 signature
3. User browser redirects to DNSP's Domain Connect UX
4. DNSP validates signature, authenticates user, verifies zone ownership, resolves template variables, detects conflicts, presents consent screen
5. User approves; DNSP applies records atomically; redirects back to SP

**Scoping and security:**

Template scope is fixed at review time — a deployed template can only modify the record types and hostnames it declares. URL signing (RS256, public key published in DNS at `{key}.{syncPubKeyDomain}`) prevents parameter tampering between SP redirect and DNSP consent screen. OAuth tokens in the async flow are scoped to the specific template and resource records.

**What this replaces:**

The manual DNS provisioning step in domain onboarding workflows. For organizations managing DNS configuration at scale — IT departments onboarding Microsoft 365 or Google Workspace across a domain fleet, web agencies configuring client zones, MSPs — Domain Connect eliminates per-registrar variation in the provisioning step and removes the human error surface from record entry.

**Relevant links:**

- IETF specification: draft-ietf-dconn-domainconnect-01
- Template repository: github.com/Domain-Connect/Templates
- Zone application library (Python): github.com/domain-connect/DomainConnectApplyZone
- Reference implementation: exampleservice.domainconnect.org

---

*Back to: [Explainers Index](./explainers.md) · [Storytelling Index](../../14_Storytelling.md)*
