# 11 — Template Reference

*Part of the [Domain Connect Knowledge Base](./00_MASTER.md)*

*Specification source: draft-ietf-dconn-domainconnect-01 (March 2026)*  
*Usage statistics: [stats.domainconnect.org](https://stats.domainconnect.org) — 720 templates as of 2026-05-14*  
*Contribution rules: [github.com/Domain-Connect/Templates README](https://github.com/Domain-Connect/Templates/blob/master/README.md)*

---

## Overview

A Domain Connect template is a JSON document with two parts:

1. **Template-level metadata** — identification, display information, behavioral flags
2. **Records array** — one or more DNS resource record definitions, each with its own fields and flags

This document is an exhaustive reference for every field in both parts. Each entry covers: purpose, allowed values, constraints, behavioral implications, and real-world use cases.

---

## Part 1: Template-Level Fields

### Quick reference

| Field | Key | Type | Required | Usage in 720 templates |
|-------|-----|------|----------|------------------------|
| Service Provider Id | `providerId` | String | REQUIRED | 720 / 720 |
| Service Provider Name | `providerName` | String | REQUIRED | 720 / 720 |
| Service Id | `serviceId` | String | REQUIRED | 720 / 720 |
| Service Name | `serviceName` | String | REQUIRED | 720 / 720 |
| Version | `version` | Integer | optional | common |
| Logo URL | `logoUrl` | String (URI) | optional | common |
| Description | `description` | String | optional | common |
| Variable Description | `variableDescription` | String | optional | rare |
| Synchronous Block | `syncBlock` | Boolean | optional | rare |
| Shared Provider Name | `sharedProviderName` | Boolean | optional | rare |
| Shared Service Name | `sharedServiceName` | Boolean | optional | rare |
| Synchronous Public Key Domain | `syncPubKeyDomain` | String | optional | **649 / 720 (90%)** |
| Synchronous Redirect Domains | `syncRedirectDomain` | String | optional | **477 / 720 (66%)** |
| Multiple Instance | `multiInstance` | Boolean | optional | rare |
| Warn Phishing | `warnPhishing` | Boolean | optional | 30 / 720 (4%) |
| Host Required | `hostRequired` | Boolean | optional | **183 / 720 (25%)** |
| Records | `records` | Array | REQUIRED | 720 / 720 |
| *(deprecated)* Shared | `shared` | Boolean | deprecated | — |

---

### `providerId`

**Type:** String  
**Required:** Yes

The unique identifier for the Service Provider that created the template. Used in the URL path when a DNS Provider exposes the template query endpoint:

```
GET /v2/domainTemplates/providers/{providerId}/services/{serviceId}
```

**Allowed values:** Must conform to the `dc-id` syntax — alphanumeric characters, hyphens, and dots; no spaces or special characters. To ensure non-coordinated uniqueness, SHOULD be the Service Provider's own domain name (e.g. `shopify.com`, `microsoft.com`).

**Example:**
```json
"providerId": "shopify.com"
```

**Caveat:** This value is permanent — changing it breaks all existing DNS Provider deployments of the template. Choose carefully; use the SP's canonical domain name, not a product name that may change.

---

### `providerName`

**Type:** String  
**Required:** Yes

The human-readable name of the Service Provider, suitable for display on the DNS Provider's consent screen. DNS Providers SHOULD display this when requesting user authorization.

**Allowed values:** Must conform to `dc-display-name` syntax — printable Unicode characters, limited length (typically ≤255 characters).

**Example:**
```json
"providerName": "Shopify"
```

**Relationship to `sharedProviderName`:** If `sharedProviderName` is `true`, the caller may supply a different `providerName` at apply time to override this value dynamically. In that case, DNS Providers should display both the override and the original.

**Caveat:** This is what users see on the consent screen. A poorly named provider reduces user trust and increases confusion. Use the recognizable brand name, not an internal identifier.

---

### `serviceId`

**Type:** String  
**Required:** Yes

The unique identifier for this specific service/template within the Service Provider's namespace. Combined with `providerId`, it forms the primary key for the template. Used in API URLs and as the OAuth scope name.

**Allowed values:** Must conform to `dc-id` syntax. Scoped to the `providerId` namespace, so uniqueness only needs to be per-provider.

**Example:**
```json
"serviceId": "website"
```

**OAuth scope:** In the asynchronous flow, the OAuth scope is derived from the `{providerId}/{serviceId}` pair, precisely limiting what the token can access.

**Caveat:** Like `providerId`, this is effectively permanent once deployed. Changing it requires deploying a new template and retiring the old one.

---

### `serviceName`

**Type:** String  
**Required:** Yes

The human-readable name of the specific service, suitable for display on the consent screen. This is what the user sees as the name of what they are connecting.

**Example:**
```json
"serviceName": "Shopify Website"
```

**Relationship to `sharedServiceName`:** If `sharedServiceName` is `true`, the caller may supply a different `serviceName` at apply time — useful for multi-tenant platforms where the same template is reused across differently branded services.

---

### `version`

**Type:** Integer (positive, no leading zeros, no fractions)  
**Required:** No

A monotonically increasing integer that identifies the version of the template content. SHOULD be incremented each time the template is updated.

**Purpose:** Coordination and transparency between the Service Provider and DNS Providers. When a SP submits an updated template, the version number signals to the DNS Provider that a review and re-deployment is needed. The DNS Provider MAY expose the version in the template query response.

**Example:**
```json
"version": 4
```

**Caveat:** This is informational — the DNS Provider is not required to enforce version sequencing or block deployments of older versions. It is primarily a communication tool, not a security mechanism.

---

### `logoUrl`

**Type:** String (URI)  
**Required:** No

A URL pointing to a logo image representing the Service Provider and/or service. The DNS Provider MAY display this logo on the consent screen to help users recognize the service they are connecting to.

**Allowed values:** Must be a valid URI with scheme `https`. No `http` URLs.

**Example:**
```json
"logoUrl": "https://cdn.example.com/logo.svg"
```

**Use case:** Logos on the consent screen increase user recognition and trust, reducing the chance that users cancel due to unfamiliarity. Services with strong brand recognition benefit most.

**Caveat:** The image must remain permanently accessible at this URL — if it goes offline, consent screens may show a broken image. Use a CDN-hosted URL, not a development or temporary endpoint.

---

### `description`

**Type:** String  
**Required:** No

A human-readable description of what the template does, intended for developer reference during template review and onboarding. NOT intended for display to end users.

**Allowed values:** Must conform to `dc-description-text` syntax.

**Example:**
```json
"description": "Connects your domain apex and www to our web hosting infrastructure. Adds DKIM key for outgoing mail."
```

**Use case:** Helps DNS Provider reviewers understand the template's intent during the onboarding/vetting process. A clear description accelerates approval and reduces back-and-forth.

---

### `variableDescription`

**Type:** String  
**Required:** No

A human-readable description of the template variables — what they are, what values are expected, and any constraints. Like `description`, intended for developer reference only, not end-user display.

**Example:**
```json
"variableDescription": "IP: the IPv4 address of the user's hosting instance. RANDOMTEXT: a one-time verification token prefixed with 'shm:'"
```

**Use case:** Particularly useful when variables have non-obvious expected formats (e.g., a token with a specific prefix, a CNAME target ending in a specific suffix). Helps DNS Providers understand what to expect during review and helps SP developers implement the integration correctly.

---

### `syncBlock`

**Type:** Boolean  
**Required:** No  
**Default:** `false`

When `true`, signals that this template does NOT support the synchronous flow. The DNS Provider MUST NOT process synchronous apply requests for this template and MUST return an error if one is received.

**Use case:** Templates that require multi-step processing or ongoing DNS management (e.g., initial verification followed by service configuration) may be asynchronous-only. Setting `syncBlock: true` makes this explicit and prevents misuse through the synchronous flow.

**Security relevance:** Some templates with significant phishing risk (see `warnPhishing`) may be locked to the asynchronous flow to ensure that the OAuth consent step provides additional controls. Setting `syncBlock: true` is one of three mitigations for template variable phishing risk (alongside URL signing and `warnPhishing`).

---

### `sharedProviderName`

**Type:** Boolean  
**Required:** No  
**Default:** `false`

When `true`, indicates that the caller MAY supply an additional `providerName` parameter at apply time, overriding or supplementing the `providerName` field in the template.

**Use case:** Multi-tenant platforms where a single Service Provider hosts services on behalf of multiple branded sub-providers. For example, a reseller platform might have one template for all resellers but display each reseller's brand name on the consent screen.

**DNS Provider behavior:** When `sharedProviderName` is set and a `providerName` parameter is provided at apply time, the DNS Provider SHOULD display both the caller-supplied name and the original template `providerName`, so users can see both the sub-brand and the underlying SP.

**Backward compatibility:** For DNS Providers prior to spec v2.2, also set the deprecated `shared` flag alongside `sharedProviderName` to ensure compatibility.

**Note:** The older `shared` field is deprecated and replaced by `sharedProviderName`. New implementations should use `sharedProviderName` only.

---

### `sharedServiceName`

**Type:** Boolean  
**Required:** No  
**Default:** `false`

When `true`, indicates that the caller MAY supply an additional `serviceName` parameter at apply time, overriding the `serviceName` field in the template.

**Use case:** Similar to `sharedProviderName` — useful for platforms that reuse one template across multiple product offerings with different display names. For example, a hosting platform that offers "Basic Hosting", "Professional Hosting", and "Enterprise Hosting" through a single template.

---

### `syncPubKeyDomain`

**Type:** String (domain name)  
**Required:** No  
**Usage: 649 out of 720 templates (90%)**

The domain name under which the Service Provider publishes its public signing key(s) as DNS TXT records. When this field is present, digital signing is **required** for synchronous apply requests — the DNS Provider MUST verify the signature and MUST reject unsigned requests.

**How it works:**
- The SP signs the apply request URL using a private key (RS256 by default)
- The corresponding public key is published in DNS at `{key-label}.{syncPubKeyDomain}`
- The apply request includes `sig=` (the signature) and `key=` (the label identifying which public key to use)
- The DNS Provider fetches the public key from DNS and verifies the signature

**Example:**
```json
"syncPubKeyDomain": "domainconnect.shopify.com"
```

The public key is then published at:
```
_dcpubkeyv1.domainconnect.shopify.com. IN TXT "p=1,a=RS256,d=<base64-key>"
```

**What this prevents:** An attacker who intercepts or crafts a redirect URL cannot modify any parameter (IP address, CNAME target, verification token) without invalidating the signature, because the signature covers all parameters.

**Key rotation:** The SP MAY publish multiple keys under different labels within `syncPubKeyDomain`. Each apply request specifies which key was used via the `key` parameter. To rotate keys, publish a new key at a new label and start signing new requests with the new key.

**Key fragmentation:** Because TXT records have a 255-byte limit per string, public keys MAY be split across multiple TXT records at the same host using the `p=` (fragment index) attribute. Fragments are reassembled in ascending `p` order.

**Mutual exclusivity with `warnPhishing`:** `syncPubKeyDomain` and `warnPhishing` MUST NOT appear in the same template. They are alternatives: `syncPubKeyDomain` provides cryptographic guarantee; `warnPhishing` is a UI-only fallback for when signing is not feasible. Setting both is invalid — linter rule **DCTL1028**.

**Template repository rule:** The template repository requires `syncPubKeyDomain` in every submitted template. The only accepted alternatives are `syncBlock: true` (restrict to async-only flow, which authenticates via OAuth instead) or `warnPhishing: true` (last resort, no cryptographic guarantee, will cause some DNS providers to reject the template by policy). Omitting `syncPubKeyDomain` without justification causes the PR to be rejected — linter rule **DCTL1029**.

**Caveat:** 90% of deployed templates use this field — it is effectively the standard. Templates without `syncPubKeyDomain` are vulnerable to URL parameter manipulation. Any template that controls where web traffic goes (A or CNAME records) should use signing.

---

### `syncRedirectDomain`

**Type:** String (comma-separated list of domain names)  
**Required:** No  
**Usage: 477 out of 720 templates (66%)**

A comma-separated list of domain names to which the DNS Provider is permitted to send the post-apply redirect in the synchronous flow. When the Service Provider supplies a `redirect_uri` parameter in the apply request, the DNS Provider MUST verify that the `redirect_uri` hostname matches one of the domains in this list.

**Purpose:** Prevents open redirect attacks, where a malicious actor crafts an apply URL with a `redirect_uri` pointing to an attacker-controlled site. Without this list, the DNS Provider cannot validate whether a redirect destination is legitimate.

**Example:**
```json
"syncRedirectDomain": "shopify.com,myshopify.com"
```

**Caveat:** This is a security control, not a routing preference. Omitting it means the DNS Provider cannot validate `redirect_uri` values — acceptable only for templates where the redirect destination is fixed or irrelevant, but risky for templates where the SP relies on the redirect to confirm success.

---

### `multiInstance`

**Type:** Boolean  
**Required:** No  
**Default:** `false`

When `true`, signals that the template is designed to be applied multiple times to the same domain and host — each application creates an independent instance rather than replacing the previous one.

**Default behavior (false):** A second apply of the same template to the same `domain`+`host` is treated as an update — the DNS Provider removes the previous instance and writes the new one.

**Multi-instance behavior (true):** Each apply creates an additive instance. The DNS Provider MUST NOT remove previous instances when a new one is applied (as long as `host` is the same). Regular conflict detection still runs between instances, so the template MUST be designed so that it does not conflict with itself.

**Use case:** Templates that configure DKIM public keys are a prime example. A domain may legitimately have multiple DKIM TXT records — one per mail service (e.g., one for transactional mail, one for marketing email). Setting `multiInstance: true` allows multiple DKIM key templates to coexist.

**Caveat:** Templates with `multiInstance` require careful conflict-rule design. Because regular conflict detection still applies, any record in the template that would conflict with an existing instance of the same template will be flagged. Template records must be idempotent-safe or use `txtConflictMatchingMode: None`.

**Note:** Multi-instance behavior only matters for DNS Providers that maintain applied template state. Providers that do not track state handle re-applies as simple zone writes regardless of this flag.

---

### `warnPhishing`

**Type:** Boolean  
**Required:** No  
**Default:** `false`  
**Usage: 30 out of 720 templates (4%)**

When `true`, signals that the template contains variable-resolved record values that could be set to point the domain at arbitrary infrastructure — and therefore cannot be fully constrained by URL signing. The DNS Provider SHOULD display additional warnings prompting the user to verify the source of the request before approving.

**The underlying risk:** A template with an A record using `%IP%` as the value is inherently open — any IP address could be substituted. If an attacker sends a user a crafted apply URL with a malicious IP address and the user approves it, the domain gets hijacked. Even with URL signing, the signed request may be legitimate but still carry a malicious value placed by a compromised SP.

**Mutual exclusivity with `syncPubKeyDomain`:** `warnPhishing` and `syncPubKeyDomain` MUST NOT appear in the same template — linter rule **DCTL1028**. `warnPhishing` is only valid when `syncPubKeyDomain` is absent. It is a last-resort fallback, not a complement to signing.

**Priority order for phishing mitigation (best to weakest):**
1. URL signing (`syncPubKeyDomain`) — cryptographic guarantee; prevents parameter tampering
2. `syncBlock: true` — prevents the synchronous flow entirely; forces OAuth with its stronger authentication
3. `warnPhishing: true` — UI-only warning; no cryptographic backing; some DNS providers will reject templates with this flag by policy

**Use case for `warnPhishing`:** Only when signing is genuinely infeasible and async-only flow is impractical. Examples: templates with variables that must be the entire record value as prescribed by an external standard, where the SP cannot implement key management.

**Caveat:** At 4% usage, `warnPhishing` is rare by design — the template repository steers authors toward signing first. If you find yourself setting this flag, reconsider whether `syncPubKeyDomain` is truly impossible to implement.

---

### `hostRequired`

**Type:** Boolean  
**Required:** No  
**Default:** `false`  
**Usage: 183 out of 720 templates (25%)**

When `true`, indicates that the template is only applicable when both `domain` AND `host` apply parameters are provided. The DNS Provider MUST reject apply requests that omit the `host` parameter for this template.

**Use case:** Templates that contain CNAME records are the most common case — CNAME records cannot be placed at the zone apex (the `@` / bare domain). If a template has a CNAME record and `host` is empty, the resulting CNAME at the apex is invalid. Setting `hostRequired: true` prevents this.

Also applies to templates designed to configure subdomain services rather than the apex, where the SP needs to guarantee that a subdomain is always specified.

**Example scenario:** A CDN service template that sets `www CNAME customer.cdn.example.com.` requires `host=www` to be passed. If the user omits the host parameter, the template would try to set `@ CNAME customer.cdn.example.com.` which is either invalid (CNAME at apex) or wrong (pointing the root domain instead of `www`).

**Caveat:** Setting `hostRequired: true` shifts the responsibility for providing a valid `host` value to the Service Provider's integration code. The SP must always include `host=` in the apply URL. Omitting this flag on templates that need it is a common integration bug.

---

### `records`

**Type:** Array of Template Record objects  
**Required:** Yes

The core of the template — the list of DNS resource records that will be written to the user's zone when the template is applied. Each element is a Template Record object (see Part 2).

Must contain at least one record. All records in the array are subject to group filtering, variable substitution, conflict detection, and zone write operations as defined in Section 10 of the spec.

---

## Part 2: Template Record Fields

Each element of the `records` array defines one DNS resource record to be applied. Records share common fields and have type-specific fields.

### Common fields (all record types)

#### `type`

**Type:** Enum / String  
**Required:** Yes

The DNS record type. Controls which additional fields are required and how conflict detection operates.

| Value | DNS type | DNS Provider support | Usage in 720 templates |
|-------|----------|---------------------|------------------------|
| `A` | IPv4 address | REQUIRED | 244 records |
| `AAAA` | IPv6 address | REQUIRED | 17 records |
| `CNAME` | Canonical name alias | REQUIRED | 519 records |
| `MX` | Mail exchange | REQUIRED | 136 records |
| `TXT` | Text record | REQUIRED | 327 records |
| `SRV` | Service locator | REQUIRED | 22 records |
| `NS` | Name server | REQUIRED | 6 records |
| `SPFM` | SPF merge (pseudo-type) | SHOULD support | 164 records |
| `REDIR301` | HTTP 301 redirect | optional extension | 16 records |
| `REDIR302` | HTTP 302 redirect | optional extension | 1 record |
| `APEXCNAME` | Apex CNAME (ANAME/ALIAS) | optional extension | 5 records |
| `CAA` | Certificate Authority Authorization | optional | 5 records |
| `TYPE{n}` | Unknown type per RFC 3597 | optional | — |

**CNAME constraint:** A CNAME record's `host` field MUST NOT be `@` or empty unless `hostRequired` is `true` in the template definition, because CNAME at the zone apex is prohibited by DNS standards.

**Unknown types:** Any IANA-registered DNS RR type name may be used. Types not natively understood by the DNS Provider are specified using the RFC 3597 `TYPE{n}` notation (e.g. `TYPE257` for CAA before it was widely supported). Support for non-core types is optional per DNS Provider.

**Extension types (`REDIR301`, `REDIR302`, `APEXCNAME`):** These are Domain Connect extensions not defined in standard DNS. They instruct the DNS Provider to configure HTTP redirects or apex aliasing using whatever mechanism the DNS Provider supports natively. DNS Provider support varies.

---

#### `host`

**Type:** String  
**Required:** Yes (for A, AAAA, CNAME, NS, TXT, MX, and unknown types; replaced by `name` for SRV)

The DNS owner name for the record, relative to the applied domain and subdomain scope. Determines where in the zone the record is written.

**Special values:**
- `@` or empty string — the zone apex (or the applied subdomain if `host` is specified in the apply request)
- A label like `www` — prepended to the domain scope: `www.example.com.`
- A trailing dot `.` suffix — treated as an absolute DNS name, used as-is
- `%domain%.` — resolves to the absolute zone apex regardless of the `host` apply parameter (useful for templates that need to write both subdomain and apex records)

**Variables:** May contain variable expressions (`%VARNAME%`), though embedding subdomain labels as variables is discouraged — see the `host` apply parameter guidance below.

**Example:**
```json
{ "type": "A", "host": "@", "pointsTo": "192.0.2.1", "ttl": 1800 }
{ "type": "CNAME", "host": "www", "pointsTo": "target.cdn.example.", "ttl": 3600 }
```

**Never write `%host%` in the `host` field:** The Domain Connect protocol automatically appends the `host` apply parameter to every record's owner name. Writing `%host%` explicitly causes the label to be doubled — e.g. `sub.sub.example.com` instead of `sub.example.com`. Remove it entirely; the protocol handles this without any explicit reference — linter rule **DCTL1024**.

**Never use a variable in `host` to target a subdomain:** Do not use `"host": "%subdomain%"` as a mechanism for making the template apply to a user-supplied subdomain. Use the `host` apply parameter of the Domain Connect protocol instead. If a variable is used in `host`, the template appears to work on first apply — but on a second application with a different variable value, DNS Providers that track template integrity will remove the records from the first application, because the label has changed. Use `multiInstance` if the standard `host` parameter is insufficient.

**Narrow variables in `host`:** When a variable in `host` is genuinely needed (e.g. a DKIM selector), fix the surrounding label parts so the variable can only resolve to a meaningful, service-specific hostname. For DKIM: use `"host": "%dkimkey%._domainkey"` rather than `"host": "%dkimkey%"`. The `._domainkey` suffix is fixed; only the selector label varies.

**Caveat on variables in `host` (general):** If `host` contains a variable, the template scope becomes indeterminate at consent time — the DNS Provider cannot predict exactly which labels will be affected until the variable is resolved. This prevents accurate conflict detection in the asynchronous flow and is therefore discouraged. Use the `host` apply parameter instead of template variables to specify subdomains.

---

#### `ttl`

**Type:** Integer or string representation of integer  
**Required:** Yes (for A, AAAA, CNAME, NS, TXT, MX, SRV; not applicable to SPFM)

Time-to-live in seconds. Controls how long the record is cached by resolvers.

**DNS Provider discretion:** The spec explicitly treats the TTL as "best effort." The DNS Provider MAY adjust the TTL to fit its own minimum/maximum constraints or TTL enumeration policy without rejecting the template. The SP should not rely on the exact TTL being honored, and MUST NOT reject responses where DNS records have been written with a different TTL.

**Variables:** Support for variables in the `ttl` field is OPTIONAL for DNS Providers. Template authors should prefer integer literals.

**Example:**
```json
"ttl": 1800
```

**Caveat:** Very short TTLs (e.g., 60 seconds) may be rounded up to the DNS Provider's minimum. Very long TTLs may be capped. Design templates assuming the TTL may be adjusted within a reasonable range (e.g., 600–86400 seconds).

---

#### `groupId`

**Type:** String  
**Required:** No

Assigns this record to a named group, enabling staged template application. When the apply request includes a `groupId` parameter, only records whose `groupId` matches are processed; records without a `groupId` are always active.

**Allowed values:** Must conform to `dc-id` syntax. MUST NOT contain variable expressions.

**Group filtering rules:**
1. A record with no `groupId` is always active, regardless of the `groupId` apply parameter
2. A record with a `groupId` is active only if its `groupId` appears in the apply request's `groupId` parameter
3. If no `groupId` is supplied in the apply request, all records are active

**Use case:** Two-phase service setup — phase 1 applies only the verification records, phase 2 applies only the service records:

```json
{ "type": "TXT", "groupId": "verify", "host": "@", "data": "%TOKEN%", "ttl": 300 }
{ "type": "MX",  "groupId": "service", "host": "@", "pointsTo": "mail.example.com", "priority": 10, "ttl": 3600 }
```

The SP applies `groupId=verify` first, waits for domain ownership confirmation, then applies `groupId=service`.

**State tracking:** When a `groupId` parameter is supplied, the apply operation is additive — only the specified group's records are written, and records from other groups that were previously written are left untouched. The DNS Provider removes only previously written records for the same group(s) before writing the new active set.

**Caveat:** If `groupId` is supplied in the apply request but no record in the template carries a matching `groupId`, the DNS Provider MUST return an error and make no zone changes. Ungrouped records do not count as a match for a specific group.

---

#### `essential`

**Type:** Enum  
**Required:** No  
**Default:** `Always`

Controls how the record participates in template integrity and conflict detection for DNS Providers that maintain applied template state.

| Value | Behavior |
|-------|----------|
| `Always` | The record is essential for the lifetime of the template. If it is modified or removed (by the user or another template), this is treated as a conflict — the entire template must be reverted or the conflicting action aborted. |
| `OnApply` | The record must be applied when the template is first applied, but may subsequently be removed or altered without triggering removal of the owning template. |

**`Always` use case:** The core records that define a service. An MX record for email routing is essential — if it is removed, the email service stops working, and the template as a whole should be removed rather than left in a broken state.

**`OnApply` use case:** Two distinct scenarios:

1. **Ephemeral records.** A TXT domain ownership verification record needs to be present at apply time, but once verification completes it may be removed. Setting `essential: OnApply` allows this without triggering template removal.

2. **User-editable records.** Records the end user should be able to modify independently after setup — for example, a DMARC policy TXT record. A user legitimately wants to change their DMARC policy from `p=none` to `p=quarantine` over time. Without `essential: OnApply`, DNS Providers tracking template state would treat this manual change as a conflict and may remove or disable the entire template. Setting `essential: OnApply` signals that the record is expected to be written at apply time but may diverge from the template value later without consequence.

```json
{
  "type": "TXT",
  "host": "@",
  "data": "%VERIFICATION_TOKEN%",
  "ttl": 300,
  "txtConflictMatchingMode": "Prefix",
  "txtConflictMatchingPrefix": "verify-token:",
  "essential": "OnApply"
}
```

**Caveat:** This field only has behavioral effect on DNS Providers that maintain applied template state. DNS Providers without state tracking ignore it. Templates relying on `OnApply` semantics for ephemeral records should communicate this expectation during the onboarding process with each DNS Provider.

---

### Record-type-specific fields

#### `pointsTo`

**Type:** String  
**Used in:** A, AAAA, CNAME, NS, MX

The target value of the record. Interpretation depends on record type:

| Type | Expected value |
|------|----------------|
| A | IPv4 address (e.g. `198.51.100.1`) |
| AAAA | IPv6 address (e.g. `2001:db8::1`) |
| CNAME | Fully qualified domain name (e.g. `target.cdn.example.com.`) |
| NS | Nameserver hostname |
| MX | Mail exchange hostname |

**Variables:** May contain variable expressions. For A/AAAA records, the entire value or a suffix of it may be variable (e.g., `198.51.100.%srv%` where `srv` resolves to a last-octet value). For CNAME/MX, the variable typically represents the full hostname or a meaningful prefix/suffix.

**Variable scope minimization:** Best practice is to minimize the variable portion. Instead of `"pointsTo": "%FULLHOSTNAME%"`, prefer `"pointsTo": "%ACCOUNT%.cdn.example.com"` where only the account-specific label is variable. This gives the DNS Provider more meaningful information during template review and limits what a bad actor could inject. A bare variable as the entire record value (`"pointsTo": "%FULLHOSTNAME%"`) is only acceptable when the full value is prescribed by an external standard and a fixed prefix is impossible — this must be justified in the PR description when submitting to the template repository.

---

#### `data`

**Type:** String  
**Used in:** TXT (required), unknown record types (required)

For TXT records: the record data in DNS presentation format. May contain quotes for multi-string records; quotes may be omitted for single strings without spaces.

**Never use `data` for SPF:** A TXT record whose `data` starts with `v=spf1` is prohibited in the template repository — linter rule **DCTL1014**. Use the `SPFM` pseudo-type instead. Domain Connect merges multiple SPFM records across templates automatically; raw SPF TXT records from different templates conflict and overwrite each other.

For unknown/unspecified record types: the canonical presentation format of the record data, following RFC 3597 generic or type-specific encoding.

**Variables:** May contain variable expressions, either as the entire value or embedded in a larger string.

**TXT record example with prefix:**
```json
{
  "type": "TXT",
  "host": "@",
  "data": "google-site-verification=%VERIFICATION_CODE%",
  "ttl": 3600,
  "txtConflictMatchingMode": "Prefix",
  "txtConflictMatchingPrefix": "google-site-verification="
}
```

**Caveat:** `data` MUST NOT be used for record types that have their own type-specific fields defined in the spec (e.g., do not use `data` on MX records — use `pointsTo` and `priority` instead). For SPFM records, use `spfRules`, not `data`.

---

#### `txtConflictMatchingMode`

**Type:** Enum  
**Used in:** TXT (optional)  
**Default:** `None`

Controls how the DNS Provider detects conflicts between this TXT record and existing TXT records at the same hostname.

| Value | Behavior |
|-------|----------|
| `None` | No conflict detection for this TXT record. The new record is added regardless of existing TXT records. |
| `All` | Any existing TXT record at the same hostname is a conflict and will be removed before this record is written. |
| `Prefix` | Only TXT records whose value starts with `txtConflictMatchingPrefix` are conflicts. Other TXT records are left untouched. |

**`None` use case:** Adding a new, independent TXT record (e.g., a DKIM key, a domain verification token that does not conflict with anything). If multiple services may add TXT records to the same hostname, `None` allows them to coexist.

**`All` use case:** Setting a TXT record that must be the only TXT record at that hostname. Rare in practice, as most domains have multiple TXT records for different purposes.

**`Prefix` use case:** Replacing a specific service's existing TXT record while leaving other services' records intact. The classic example is domain ownership verification tokens that use a service-specific prefix:

```json
{
  "type": "TXT",
  "host": "@",
  "data": "shopify-verification=%TOKEN%",
  "ttl": 600,
  "txtConflictMatchingMode": "Prefix",
  "txtConflictMatchingPrefix": "shopify-verification="
}
```

This removes only Shopify's previous verification token, leaving SPF, DKIM, and other services' records untouched.

**Caveat:** Using `All` at the zone apex would remove SPF, DKIM, and all other TXT records — almost certainly unintended. Use `All` only on specific subdomains where you know the TXT record should be exclusive, or when the template is designed to replace all existing TXT records at that label.

---

#### `txtConflictMatchingPrefix`

**Type:** String  
**Used in:** TXT (required when `txtConflictMatchingMode` is `Prefix`)

The prefix string used to identify which existing TXT records are conflicts when `txtConflictMatchingMode` is `Prefix`. Only TXT records at the same hostname whose value starts with this prefix are considered conflicts.

**Must be:** Consistent with the `data` field — the prefix should match the beginning of the `data` value. If `data` is `"shopify-verification=%TOKEN%"`, the prefix should be `"shopify-verification="`.

**Caveat:** The matching is exact string prefix matching on the full TXT record value. If an existing TXT record has leading whitespace or uses a different quoting style, the prefix match may fail. Keep prefixes short, unambiguous, and ASCII-safe.

---

#### `priority`

**Type:** Integer or string representation of integer  
**Used in:** MX (required), SRV (required)

For MX records: the mail exchange preference value. Lower values indicate higher preference. Standard values range from 0 to 65535.

For SRV records: the priority of the target host. Lower values are preferred.

**Variables:** Support for variables in `priority` is OPTIONAL for DNS Providers.

**Example (MX):**
```json
{ "type": "MX", "host": "@", "pointsTo": "mail.example.com", "priority": 10, "ttl": 3600 }
```

---

#### `weight`

**Type:** Integer or string representation of integer  
**Used in:** SRV (required)

The weight for load balancing among SRV records with the same priority. Higher weights are selected more frequently. Range: 0–65535.

**Variables:** Support for variables in `weight` is OPTIONAL for DNS Providers.

---

#### `port`

**Type:** Integer or string representation of integer  
**Used in:** SRV (required)

The TCP/UDP port on which the service is available. Range: 0–65535.

**Variables:** Support for variables in `port` is OPTIONAL for DNS Providers.

---

#### `protocol`

**Type:** String  
**Used in:** SRV (required)

The transport protocol for the SRV record. Must conform to `dc-srv-protocol` syntax.

**Common values:** `_tcp`, `_udp`, `_sctp`

**Example:**
```json
{ "type": "SRV", "name": "@", "service": "_sip", "protocol": "_tcp", "priority": 10, "weight": 20, "port": 5060, "target": "sipserver.example.com.", "ttl": 3600 }
```

---

#### `service`

**Type:** String  
**Used in:** SRV (required)

The symbolic service name for the SRV record (e.g., `_sip`, `_xmpp-client`, `_autodiscover`). Must conform to `dc-srv-service` syntax.

---

#### `name`

**Type:** String  
**Used in:** SRV (replaces `host` for SRV records)

The DNS owner name for the SRV record, relative to the applied domain scope. Same semantics as `host` for other record types — `@` or empty means the zone apex of the applied scope.

---

#### `target`

**Type:** String  
**Used in:** SRV (required)

The hostname of the target providing the service, per RFC 2782. Must conform to `dc-pointsto-tmpl` syntax after variable substitution, or be the single label `"."` to explicitly indicate that the service is not available at this name.

**Variables:** May contain variable expressions.

---

#### `spfRules`

**Type:** String  
**Used in:** SPFM (required)

The SPF mechanism and modifier terms to be merged into the domain's SPF TXT record. Contains everything that would go between `v=spf1` and `all` in a standard SPF record.

**Allowed content:** SPF mechanism and modifier terms as defined in RFC 7208 Section 5. Must NOT include the version prefix (`v=spf1`) or the terminating `all` qualifier.

**Example:**
```json
{
  "type": "SPFM",
  "host": "@",
  "spfRules": "include:spf.protection.outlook.com"
}
```

This instructs the DNS Provider to merge `include:spf.protection.outlook.com` into the existing SPF record:
- If no SPF record exists: creates `v=spf1 include:spf.protection.outlook.com ~all`
- If an SPF record exists: merges the mechanism in, producing e.g. `v=spf1 include:_spf.google.com include:spf.protection.outlook.com ~all`

**DNS Provider MUST validate** the `spfRules` syntax before merging.

**Conflict policy for SPFM:** When multiple SPFM records from different templates specify the same mechanism with different policies (e.g., one says `~all` and another says `-all`), the DNS Provider SHOULD apply the least restrictive policy (`~all` preferred over `-all`; `?` preferred over `~`).

**Caveat:** The resulting SPF TXT record is considered non-essential — users may override or remove the merged SPF record without triggering removal of the owning template. Additionally, if the existing SPF record is malformed in a way that prevents merging, the DNS Provider must handle this as a conflict and surface it to the user.

Service Providers MUST NOT check the content of the SPF TXT record for an exact match, since the DNS Provider's merging strategy and user modifications will affect the final value.

---

## Part 3: Variable System

### Variable syntax

Template variable expressions use `%VARNAME%` notation:
- Variable names are case-insensitive alphanumeric identifiers
- The entire expression `%VARNAME%` is replaced with the value passed by the SP at apply time
- The special variable `@` is a shorthand for `%fqdn%.` (the fully qualified applied domain)

**Two notation systems exist to prevent injection:**
- `%VARNAME%` — for Service Provider-defined variables (values passed in the apply request)
- `{variable}` — reserved exclusively for RFC 6570 URI Template syntax in protocol-level URL construction

**Built-in variables (reserved, cannot be used as template variable names):**

| Variable | Value |
|----------|-------|
| `%domain%` | The zone apex (e.g. `example.com`) |
| `%host%` | The subdomain label (e.g. `www`; empty if none) |
| `%fqdn%` | The fully qualified applied scope (e.g. `www.example.com` or `example.com` if no host) |
| `@` | Shorthand for `%fqdn%.` (with trailing dot — absolute DNS name) |

**Variable scope minimization principle:** Variables should be constrained to as small a portion of the record value as possible. Instead of `"pointsTo": "%FULLHOSTNAME%"`, prefer `"pointsTo": "%ACCOUNT%.cdn.example.com"` where the variable carries only the variable portion. This:
- Gives the DNS Provider better visibility into the template's intent during review
- Reduces the attack surface for phishing (a bad actor can only inject the variable portion, not the entire value)
- Makes the template easier to understand and verify

---

## Annotated Full Template Example

```json
{
  "providerId": "example.com",
  "providerName": "Example Web Hosting",
  "serviceId": "hosting",
  "serviceName": "WordPress by example.com",
  "version": 1,
  "logoUrl": "https://www.example.com/images/logo.png",
  "description": "Connects your domain to our WordPress hosting",
  "syncPubKeyDomain": "domainconnect.example.com",
  "syncRedirectDomain": "example.com",
  "hostRequired": false,
  "warnPhishing": false,
  "records": [
    {
      "type": "A",
      "groupId": "service",
      "host": "@",
      "pointsTo": "%IP%",
      "ttl": 1800,
      "essential": "Always"
    },
    {
      "type": "CNAME",
      "groupId": "service",
      "host": "www",
      "pointsTo": "%IP%.hosting.example.com",
      "ttl": 1800,
      "essential": "Always"
    },
    {
      "type": "SPFM",
      "groupId": "service",
      "host": "@",
      "spfRules": "include:spf.example.com"
    },
    {
      "type": "TXT",
      "groupId": "verify",
      "host": "@",
      "data": "example-verify=%VERIFICATION_CODE%",
      "ttl": 300,
      "txtConflictMatchingMode": "Prefix",
      "txtConflictMatchingPrefix": "example-verify=",
      "essential": "OnApply"
    }
  ]
}
```

This template:
- Requires URL signing (`syncPubKeyDomain`)
- Validates the redirect destination (`syncRedirectDomain`)
- Uses two groups: `verify` (applied first, verification token) and `service` (applied after verification, actual hosting records)
- Uses SPFM to avoid SPF conflicts
- Marks the verification TXT as `OnApply` (can be removed after verification)
- Marks the A and CNAME as `Always` essential (removing them breaks the service)

---

---

## Part 4: Contributing a Template — Process and Quality Rules

*Source: [github.com/Domain-Connect/Templates README](https://github.com/Domain-Connect/Templates/blob/master/README.md)*

The template repository at [github.com/Domain-Connect/Templates](https://github.com/Domain-Connect/Templates) is the canonical source for all Domain Connect templates. Contributing a new or updated template follows a defined process with binding quality rules enforced by a linter and PR review.

---

### Submission process

**Step 1 — Create and test your template in the Online Editor**

The [Online Editor](https://domainconnect.paulonet.eu/dc/free/templateedit) is the required starting point. It provides:
- Real-time syntax checking against the JSON schema
- Variable substitution testing with custom input values
- Group filtering testing
- Apex and subdomain (`host` parameter) testing

After testing, click **"Copy Markdown"** to generate a shareable link to your test results. This link is required in the PR.

> Pull Requests without a link to Online Editor test results will not be reviewed. Test results must match the submitted template exactly.

**Step 2 — Name the file correctly**

Template files must be named `{providerId}.{serviceId}.json` and placed in the root of the repository.

Example: `shopify.com.website.json`

**Step 3 — Open a Pull Request using the PR template**

The repository provides a PR template that loads automatically when opening a new PR on GitHub. It must be filled in completely — no sections may be skipped or removed. The Online Editor test link goes in the designated field.

---

### Quality rules (binding)

These rules are enforced by the linter ([github.com/Domain-Connect/dc-template-linter](https://github.com/Domain-Connect/dc-template-linter)) and PR review. PRs that violate them are rejected or sent back for revision.

#### Rule 1 — Always set `syncPubKeyDomain`

Every template must have `syncPubKeyDomain`. Many DNS providers reject templates without it.

**Exceptions** (must be justified in the PR description):
- Set `syncBlock: true` to restrict to async flow only (authenticates via OAuth, no key needed). Note: async flow has significantly lower DNS provider support, requires bilateral OAuth setup per provider, and is never automatic.
- Set `warnPhishing: true` as a last resort when signing and async are both infeasible. This provides no cryptographic guarantee and some providers will reject it by policy.

*Linter: [DCTL1029](https://github.com/Domain-Connect/dc-template-linter/wiki/DCTL1029)*

#### Rule 2 — Never set `syncPubKeyDomain` and `warnPhishing` together

They are mutually exclusive. Remove `warnPhishing` whenever `syncPubKeyDomain` is present.

*Linter: [DCTL1028](https://github.com/Domain-Connect/dc-template-linter/wiki/DCTL1028)*

#### Rule 3 — Set `syncRedirectDomain` when using `redirect_uri`

Required whenever the template uses the `redirect_uri` parameter in the synchronous flow. Providers that enforce this field reject the flow without it.

#### Rule 4 — Never use a TXT record for SPF — use SPFM

A TXT record whose `data` starts with `v=spf1` is prohibited. Use the `SPFM` record type at the apex instead. Domain Connect merges SPFM records from multiple templates automatically; raw SPF TXT records conflict and overwrite each other.

*Linter: [DCTL1014](https://github.com/Domain-Connect/dc-template-linter/wiki/DCTL1014)*

#### Rule 5 — Set `txtConflictMatchingMode` on TXT records that must be unique

Required on any TXT record that must be unique per label or content prefix — for example, DMARC records, domain verification tokens. Without it, applying the template can create duplicates or conflict unexpectedly with existing records.

#### Rule 6 — Scope variables narrowly in record values

Prefer embedding variables in a fixed prefix (`"@ TXT myservice-verify=%token%"`) over a bare variable as the entire record value (`"@ TXT %token%"`). A bare variable allows any arbitrary string to be injected, increases conflict risk with other templates, and makes the template harder to review.

**Exception:** Bare variables are acceptable when the full record value is prescribed by an external standard and cannot carry a prefix. Justify this in the PR description.

#### Rule 7 — Scope variables narrowly in the `host` field

When a variable must appear in `host`, fix the surrounding label parts. For DKIM: `"host": "%dkimkey%._domainkey"` — the selector is variable, but `._domainkey` is fixed, making the record type unambiguous. A fully bare host variable (`"host": "%anything%"`) allows records to be created at arbitrary labels anywhere under the domain.

**Exception:** Accepted when the subdomain name itself is genuinely user-supplied with no predictable fixed suffix. Justify in the PR description.

#### Rule 8 — Never use a `host` variable to target a subdomain

Do not use `"host": "%subdomain%"` to make a template apply to a user-chosen subdomain. Use the `host` apply parameter of the Domain Connect protocol instead. A variable in `host` for subdomain targeting causes DNS Providers with template state tracking to remove records from a prior application when the variable value changes on re-apply.

If the `host` parameter alone is insufficient, use `multiInstance`.

#### Rule 9 — Never write `%host%` in the `host` attribute

The protocol appends the `host` apply parameter automatically. Writing `%host%` in the template's `host` field causes it to be doubled in the resulting DNS name.

*Linter: [DCTL1024](https://github.com/Domain-Connect/dc-template-linter/wiki/DCTL1024)*

#### Rule 10 — Set `essential: OnApply` on records the user may need to modify

Any record that an end user should be able to change or remove independently after setup — such as a DMARC policy TXT record — must be marked `"essential": "OnApply"`. Without it, DNS Providers tracking template state treat a manual change to that record as a conflict and may disable the entire template.

---

### Template validation tools

**JSON Schema validation:** The repository includes `template.schema` for schema-based validation. Passing the schema check is required for PR acceptance.

**Linter:** [github.com/Domain-Connect/dc-template-linter](https://github.com/Domain-Connect/dc-template-linter) checks for the quality rules above and additional issues. Run it locally before submitting a PR.

**Online Editor:** [domainconnect.paulonet.eu/dc/free/templateedit](https://domainconnect.paulonet.eu/dc/free/templateedit) — required for PR submission; provides interactive syntax checking and testing.

---

*Previous: [10 — Key Messages](./10_Key_Messages.md) | Back to: [00 — Master Index](./00_MASTER.md)*
