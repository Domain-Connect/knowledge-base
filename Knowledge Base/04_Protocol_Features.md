# 04 — Protocol Features Deep Dive

*Part of the [Domain Connect Knowledge Base](./00_MASTER.md)*

---

## Feature Summary

Domain Connect is designed to handle the real-world complexity of DNS configuration. Beyond the basic "create some records" operation, it includes several sophisticated features that address common pain points in DNS management.

| Feature | Purpose |
|---------|---------|
| Template system | Standardized, pre-approved DNS configuration contracts |
| Two-flow architecture | Synchronous (one-time) and asynchronous (ongoing) |
| DNS Provider discovery | Automatic detection of protocol support via `_domainconnect` record |
| Variable substitution | Dynamic values in templates (IP addresses, verification tokens) |
| Conflict resolution | Rules for handling existing DNS records |
| SPF TXT record merging | Combining SPF records from multiple services without conflicts |
| Ephemeral records | Temporary records (e.g., domain verification) that auto-expire |
| URL signature protection | Cryptographic signing of redirect URLs to prevent tampering |
| Template groups | Staged application of DNS configuration in multiple steps |
| Scope minimization | Limiting changes to exactly what the service needs |

---

## 1. Template System

Templates are JSON documents that serve as the formal contract between a Service Provider and a DNS Provider. A template fully describes:

- **What records to create** (record type, hostname, value, TTL)
- **What variables are needed** (dynamic values supplied at runtime)
- **How to handle conflicts** (what to do if records already exist)
- **Identification** (provider ID, service ID — used in URLs and OAuth scope)
- **Display metadata** (provider name, service name, logo URL, description)

Templates are versioned. The `version` field is an integer incremented with each update, providing a simple coordination mechanism between providers.

**Template scope minimization** is a design principle: templates SHOULD request only the minimum set of DNS records and variables needed for the service to function. This limits the blast radius if anything goes wrong and makes the user consent screen more understandable.

---

## 2. Two-Flow Architecture

### Synchronous Flow
- **When:** One-time service setup where the user is present
- **How:** HTTP redirect with template ID + variables in the URL → user authenticates → consents → DNS updated → redirect back
- **Best for:** Website builders, email setup, basic service integrations
- **User experience:** Single session, typically completes in 30 seconds

### Asynchronous Flow (OAuth)
- **When:** Multi-step setup, or ongoing DNS management needed
- **How:** OAuth 2.0 authorization grant → access token issued → SP can make API calls over time
- **Best for:** Complex setups (e.g., first verify ownership, then configure MX), dynamic DNS, services that update their infrastructure
- **User experience:** User approves once; subsequent DNS changes happen in the background

A DNS Provider MAY implement only the synchronous flow. The synchronous flow is RECOMMENDED as it covers the vast majority of use cases. Service Providers may use either flow, or both.

---

## 3. DNS Provider Discovery

**The `_domainconnect` DNS record** is the entry point for the entire protocol. When a user enters their domain at a Service Provider:

1. SP looks up `_domainconnect.<domain>` as a TXT record
2. The value of the TXT record contains the URL fragment pointing to the DNS Provider's API
3. SP fetches the full "settings" JSON document from that endpoint
4. Settings document contains:
   - `urlSyncUX`: endpoint for the synchronous flow
   - `urlAsyncUX`: endpoint for the asynchronous OAuth flow
   - `urlAPI`: endpoint for the asynchronous API
   - `providerName`: human-readable DNS Provider name
   - `providerDisplayName`: display name for UI
5. SP then checks whether its specific template is supported by calling `GET /domainTemplates/providers/{providerId}/services/{serviceId}`

If at any step the protocol fails (no `_domainconnect` record, settings unavailable, template not found), the Service Provider falls back gracefully to manual instructions.

---

## 4. Variable Substitution

Templates frequently need dynamic values — values that differ per-user or per-deployment:

- The IP address of the service's server
- A unique verification token for domain ownership checks
- A CNAME target specific to the user's account

These are expressed as **named variables** in the template using `%VARIABLENAME%` notation:

```json
{
  "type": "A",
  "host": "@",
  "pointsTo": "%IP%",
  "ttl": "600"
}
```

The Service Provider passes variable values in the redirect URL:
```
?domain=example.com&IP=198.51.100.1&RANDOMTEXT=abc123
```

**Two notation systems are intentionally used** to prevent injection attacks:
- `{variable}` (RFC 6570 URI Template syntax) — used for protocol-level URL templates defined in the specification
- `%VARIABLE%` — used for Service Provider-defined template variables and dynamic elements

This distinction ensures that a misconfigured implementation cannot accidentally inject template variables into protocol-level URL components.

**Built-in variables:** The protocol defines reserved variables like `domain` and `host` that cannot be used as template variable names.

---

## 5. Conflict Detection and Resolution

When a template is applied to a zone, the DNS records it wants to create may conflict with records already in the zone. Domain Connect provides fine-grained control over how these conflicts are handled.

### Conflict detection by record type

**For A and AAAA records:**

- A conflict exists if a record with the same hostname already exists
- The template can specify whether to replace existing records or abort

**For CNAME records:**

- CNAME records cannot coexist with other records at the same hostname
- Domain Connect treats any existing record at the same hostname as a conflict

**For MX records:**

- Conflicts are detected at the hostname level
- The template controls whether existing MX records should be replaced

**For TXT records (special handling):**

The `txtConflictMatchingMode` field controls TXT conflict detection:
- `None` — no conflict detection; add the new record regardless
- `All` — any existing TXT record at this hostname is a conflict
- `Prefix` — only TXT records starting with `txtConflictMatchingPrefix` are conflicts (see SPF merging below)

### Essential flag
Each record in a template has an `essential` attribute:
- `Always` (default) — this record is essential; if it conflicts and cannot be applied, abort the entire template application
- `OnApply` — this record should be applied if possible, but its failure does not block the rest of the template

This allows templates to have "nice to have" records (e.g., CAA records for certificate issuance) that don't block the main service setup if they conflict.

### Force flag
The Service Provider can include a `force=1` parameter in the redirect URL to override conflict detection and replace existing records. This is typically used for re-configuration scenarios.

---

## 6. SPF TXT Record Merging

**The problem:** Multiple services may need to add their own SPF (Sender Policy Framework) entries to a domain's TXT records. SPF requires exactly one TXT record containing all authorized senders. A naive implementation would create multiple SPF records, which is invalid and breaks email delivery.

**Domain Connect's solution:** The `SPFM` pseudo-record type handles SPF merging automatically.

A template can specify an SPFM record:
```json
{
  "type": "SPFM",
  "host": "@",
  "spfRules": "include:spf.protection.outlook.com"
}
```

When applying this record, the DNS Provider:
1. Checks if an SPF record already exists at the hostname
2. If yes, **merges** the new `include:` mechanism into the existing SPF record
3. If no, creates a new SPF TXT record

This means a domain can have both Microsoft 365 and Google Workspace configured for email security without breaking either service's SPF requirement.

**Example:**

```
Before: v=spf1 include:_spf.google.com ~all
After:  v=spf1 include:_spf.google.com include:spf.protection.outlook.com ~all
```

---

## 7. Ephemeral Records

Some service configurations require temporary DNS records — typically for domain ownership verification. A service might need to place a TXT record to prove you control the domain, then delete it once verification is complete.

Domain Connect supports ephemeral records through the `essential: "OnApply"` flag combined with template state tracking. The DNS Provider can be instructed to apply a record temporarily and remove it after a specified condition (e.g., after the template is reverted or after the verification step completes).

This eliminates orphaned verification records that would otherwise accumulate in DNS zones over time.

---

## 8. URL Signature Protection

To prevent a malicious actor from crafting a fraudulent redirect URL that tricks a user into configuring DNS for a different service, Domain Connect supports **cryptographic URL signing**.

**How it works:**

1. The Service Provider generates a signature over the redirect URL using a private key
2. The Service Provider publishes the corresponding public key in DNS (at a subdomain like `_dck1.<provider-domain>.`)
3. The redirect URL includes the signature and a key identifier
4. The DNS Provider fetches the public key from DNS and verifies the signature before processing the request

**What this prevents:** A bad actor cannot modify the URL parameters (e.g., change the IP address to redirect the domain to their server) without invalidating the signature.

**Template-level control:** Each template specifies whether signing is required (`warnPhishing: true` enables phishing warnings; templates can require signed requests). This allows low-risk templates to work without signing while high-risk templates (those that affect where web traffic goes) can require it.

**Public key DNS record format:**

```
_dck1.exampleservice.domainconnect.org. IN TXT "p=<base64-encoded-public-key>"
```

---

## 9. Template Groups

A service may need to apply DNS configuration in multiple stages. For example:
1. First, create a TXT record to prove domain ownership
2. After verification, create MX and CNAME records to configure the actual service

Template groups (`groupId`) enable this. Records in a template can be assigned to named groups. When applying the template, the Service Provider can specify which groups to apply:

```
GET /apply?domain=example.com&groupId=verification  → applies only verification records
GET /apply?domain=example.com&groupId=service        → applies only service records
```

Both groups are part of the same template (same service), so they share conflict resolution rules and appear as a single service in the DNS Provider's tracking.

---

## 10. Template State Tracking

DNS Providers are expected to track which templates have been applied to which domains. This enables:

- **Conflict detection across multiple services:** If Service A already set a CNAME at `www.example.com`, Service B's attempt to set a different CNAME at the same label can be detected and handled appropriately
- **Revert capability:** When a user disconnects a service, the DNS Provider knows exactly which records were added by that service and can remove only those records
- **Multi-instance support:** Some records can have multiple instances (e.g., multiple DKIM TXT records for different email providers); template state tracks which instance belongs to which service

---

## Supported DNS Record Types

Domain Connect supports all standard DNS record types that may be needed for service integrations:

| Record type | Common use |
|-------------|-----------|
| A | IPv4 address — website hosting |
| AAAA | IPv6 address — website hosting |
| CNAME | Alias — subdomain redirects, CDN |
| MX | Mail exchange — email delivery |
| TXT | Text — SPF, DKIM, domain verification |
| SRV | Service locator — VoIP, messaging |
| NS | Nameserver delegation |
| SPFM | Pseudo-type — SPF merging (Domain Connect extension) |
| TYPE{n} | Unknown types per RFC 3597 — future-proofing |

---

*Previous: [03 — How It Works](./03_How_It_Works.md) | Next: [05 — Use Cases](./05_Use_Cases.md)*
