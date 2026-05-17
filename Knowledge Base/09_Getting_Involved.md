# 09 — Getting Involved

*Part of the [Domain Connect Knowledge Base](./00_MASTER.md)*

---

## Overview

Domain Connect is an open standard with open-source reference implementations, a public template registry, and an active IETF working group. There are three distinct ways to get involved: implement the protocol (as a DNS Provider or Service Provider), participate in IETF standardization, or contribute to the open-source ecosystem.

---

## Implementing as a DNS Provider

DNS Providers are the server side of Domain Connect. Implementing Domain Connect means hosting the API that Service Providers redirect users to, presenting the consent screen, and applying DNS changes to user zones.

### What implementation involves

**1. Discovery endpoint**

Publish a `_domainconnect` TXT record pointing to your API base URL. This signals to all Service Providers that your zones support Domain Connect.

**2. Settings document (discovery document)**

Serve a JSON document at a standardized URL containing your API endpoints:
- `urlSyncUX` — the synchronous flow endpoint
- `urlAsyncUX` — the OAuth authorization endpoint
- `urlAPI` — the asynchronous API endpoint
- Provider display name and metadata

**3. Template hosting**

Accept, vet, store, and serve templates from Service Providers. When a Service Provider queries whether you support their template, return an appropriate response. You control which templates you deploy.

**4. Synchronous flow endpoint**

Handle redirect requests from Service Providers: authenticate the user, verify zone ownership, display the consent screen (listing the DNS records that will be changed), and apply the approved changes.

**5. Asynchronous flow (OAuth, optional but recommended)**

Implement an OAuth 2.0 authorization flow. Issue tokens scoped to specific templates and zones. Expose the API endpoint that allows Service Providers to apply templates using tokens.

**6. Template vetting process**

Establish your process for reviewing and approving Service Provider templates before deployment. This is the critical trust anchor of the protocol — it must be taken seriously.

### Implementation effort

The implementation investment is front-loaded. Once the core protocol is implemented, each new Service Provider is just a new template — no additional code changes. The reference implementation and specification together provide enough detail to build a conforming implementation without requiring bilateral coordination with any Service Provider.

**Reference implementations and tooling:** Available at [github.com/domain-connect](https://github.com/domain-connect)

**Specification:** `draft-ietf-dconn-domainconnect-01` — available at the IETF Datatracker

---

## Implementing as a Service Provider

Service Providers are the client side of Domain Connect. Implementing as a Service Provider means creating a template for your service and integrating the discovery and redirect flow into your product.

### What implementation involves

**1. Create your template**

Define a JSON template that describes:
- Your `providerId` and `serviceId` (unique identifiers for your organization and this specific service)
- The DNS records your service requires (A, AAAA, CNAME, MX, TXT, SRV, etc.)
- The variables your template needs at runtime (e.g., `%IP%`, `%VERIFICATION_TOKEN%`)
- Conflict resolution rules (how to handle existing records)
- Template metadata (display name, logo URL, description for the consent screen)
- Whether URL signing is required (`syncPubKeyDomain`)

**2. Submit your template to DNS Providers**

Contact DNS Providers you want to support and submit your template for their review and deployment. The template repository at `domainconnect.org` and on GitHub serves as a reference, but DNS Providers deploy templates through their own onboarding process.

**3. Implement the discovery flow**

In your product flow, when a user enters a domain name:
1. Look up `_domainconnect.<domain>` as a TXT record
2. Fetch the DNS Provider's settings document
3. Check whether your template is supported (`GET /domainTemplates/providers/{providerId}/services/{serviceId}`)
4. If supported, present the "Connect automatically" option; otherwise, fall back to manual instructions

**4. Implement the redirect**

When the user clicks "Connect," redirect them to the DNS Provider's synchronous flow URL with:
- The domain and optional host parameters
- Your template variable values
- A cryptographic signature (if your template requires it)

**5. Handle the post-connection callback**

After the DNS Provider redirects the user back, verify that DNS changes have propagated before activating the service.

### Template design principles

- **Scope minimization:** Request only the minimum records needed for your service
- **Sign your URLs:** Use the signing mechanism for templates that affect web traffic (A, AAAA, CNAME records)
- **Document your variables:** Each variable should be clearly named and meaningful
- **Use SPFM, not TXT SPF:** If your service requires SPF, use the `SPFM` pseudo-record type to enable proper merging rather than creating a new SPF TXT record

---

## Participating in IETF Standardization

The DCONN (Domain Connect) working group at the IETF is the venue for shaping the protocol's future. Participation is open to anyone; IETF membership is not required.

### Ways to participate

**Mailing list**

The primary discussion channel is the DCONN working group mailing list. All substantive technical discussion about the specification happens here. Subscribe and participate at:
`https://datatracker.ietf.org/wg/dconn/about/`

**Read and comment on the draft**

The current specification is available at the IETF Datatracker. Submit feedback as GitHub issues on the specification repository or as IETF review comments.

**Attend working group sessions**

The DCONN WG meets at IETF meetings (three per year). Sessions are open and can be attended in person or remotely via meetecho. Upcoming meetings are listed on the WG page.

**Submit implementation feedback**

Organizations that have implemented the protocol are especially valuable participants. Implementation experience surfaces specification ambiguities, gaps in security guidance, and interoperability issues that are invisible in theoretical review.

### What the working group is currently working on

As of mid-2026, the working group is focused on:
- Resolving open issues from the -01 draft review
- Expanding and refining the security considerations section
- Clarifying ambiguities surfaced by implementation reports
- Progressing toward Working Group Last Call

Organizations with concerns about specific protocol aspects — security model, extended use cases like DNSSEC bootstrapping, interoperability with private/enterprise DNS — should raise them in the working group rather than treating them as blockers.

---

## Community Resources

**Official website:** [domainconnect.org](https://domainconnect.org)  
Comprehensive technical documentation, implementation guides for both DNS providers and service providers, and the template registry.

**GitHub:** [github.com/domain-connect](https://github.com/domain-connect)  
Open-source reference implementations, the template repository, specification drafts, and the issue tracker.

**IETF Datatracker:** [datatracker.ietf.org/wg/dconn/about/](https://datatracker.ietf.org/wg/dconn/about/)  
Working group page with mailing list, current drafts, and meeting materials.

**LinkedIn community:** [linkedin.com/company/domain-connect/](https://linkedin.com/company/domain-connect/)  
Practitioners, implementers, and advocates sharing experience and news.

---

## Getting Started: A Practical Path

**For DNS Providers that want to implement:**

1. Read the specification (`draft-ietf-dconn-domainconnect-01`)
2. Review the reference implementation at github.com/domain-connect
3. Identify which Service Provider templates are most requested by your customers (Microsoft 365 and Google Workspace are typically the highest demand)
4. Implement the synchronous flow first — it covers the majority of use cases
5. Define your template vetting process and submit it to your team for review
6. Onboard your first template and run a pilot

**For Service Providers that want to implement:**

1. Write your template JSON based on the specification and the template examples in the GitHub repository
2. Reach out to the DNS Providers most used by your customers and submit your template for review
3. Integrate the discovery flow into your product
4. Test the full flow with at least one DNS Provider implementation before general availability

**For organizations evaluating adoption:**

1. Check whether you already have `_domainconnect` TXT records in your zones (if you're a registrar or DNS provider) — if so, customers are already trying to use Domain Connect with you
2. Review the template registry to understand which services your customers are likely trying to connect
3. Connect with the DCONN working group mailing list to get current information on the specification status

---

*Previous: [08 — Security Model](./08_Security_Model.md) | Next: [10 — Key Messages](./10_Key_Messages.md)*
