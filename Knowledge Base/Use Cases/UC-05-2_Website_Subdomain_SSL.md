# UC-05-2: Website Hosting — Subdomain with SSL Certificate via DNS-01

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**Related:** [UC-05: Website Hosting — Subdomain / CNAME](./UC-05_Website_Hosting_Subdomain.md)  
**DNS records used:** CNAME (subdomain), TXT (`_acme-challenge` at apex)  
**Complexity:** Medium

---

## Use Case Description

A service provider hosts a website at a user-specified subdomain and needs to issue a TLS certificate for that subdomain automatically, using the ACME DNS-01 challenge. The platform cannot use HTTP-01 (no traffic reaches it yet when the certificate is issued) or TLS-ALPN-01 (same reason). DNS-01 requires placing a TXT record at `_acme-challenge.<subdomain>` before the certificate is issued.

The challenge is that `_acme-challenge.<subdomain>` sits under the user's domain — the platform has no write access to it. Normally, this forces the user to manually place a TXT record as a separate step, or the platform must ask for broad DNS write access.

Domain Connect solves this cleanly: the template places both the CNAME for the subdomain **and** the ACME challenge TXT record in one atomic consent-and-approve flow. The certificate can be issued immediately after the template is applied, with no further user interaction.

An additional refinement is available when the platform delegates ACME validation to its own infrastructure via a CNAME at `_acme-challenge`: instead of placing the TXT value directly, the template creates a CNAME that points `_acme-challenge.<subdomain>` to a provider-controlled hostname. This enables the provider to rotate challenge tokens and renew certificates without any further DNS changes.

Typical products in this category:
- App deployment platforms (JAMstack, serverless) that issue certificates per custom domain
- SaaS platforms with custom domain features requiring HTTPS from day one
- Website builders where TLS is provisioned automatically on domain connection
- Any platform using Let's Encrypt or another ACME CA for automated certificate management

---

## Value Added for the End User

Without Domain Connect, automated HTTPS on a custom subdomain typically requires a two-step process:
1. Point the subdomain CNAME at the platform
2. Manually place an `_acme-challenge` TXT record (or complete an HTTP-01 challenge, which fails if the CNAME isn't fully propagated yet)

Step 2 requires the user to return to their DNS panel, find the right instructions, place a time-limited TXT record, and then trigger certificate issuance — a confusing, error-prone flow that many users cannot complete. HTTP-01 as an alternative often fails silently because certificate issuance is attempted before DNS has propagated.

With a Domain Connect template combining the CNAME and the ACME TXT record, the user approves one consent screen and the platform can immediately begin certificate issuance. There is no second DNS step, no waiting for the user to return, and no race condition between CNAME propagation and certificate issuance.

Key benefits:
- HTTPS is provisioned in the same flow as DNS — no second step for the user
- No HTTP-01 race condition: DNS-01 validation does not depend on traffic reaching the server
- ACME CNAME delegation pattern enables fully automated certificate renewal without further DNS changes
- The platform controls the challenge token entirely — no credential sharing required

---

## Example Template — Direct TXT Placement

The platform places the ACME challenge TXT record directly. Suitable for one-time certificate issuance or if the platform re-applies the template on renewal.

```json
{
  "providerId": "appplatform.example",
  "providerName": "Acme AppPlatform",
  "serviceId": "custom-domain-ssl",
  "serviceName": "Acme AppPlatform Custom Domain with SSL",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.appplatform.example",
  "syncRedirectDomain": "dashboard.appplatform.example",
  "hostRequired": true,
  "description": "Points a subdomain to your Acme AppPlatform deployment and provisions an HTTPS certificate.",
  "records": [
    {
      "groupId": "cname",
      "type": "CNAME",
      "host": "@",
      "pointsTo": "%cnameTarget%",
      "ttl": 600
    },
    {
      "groupId": "acme",
      "type": "TXT",
      "host": "_acme-challenge.%domain%.",
      "data": "%acmeChallenge%",
      "ttl": 300
    }
  ]
}
```

---

## Example Template — ACME CNAME Delegation (Recommended)

The platform creates a CNAME at `_acme-challenge.<subdomain>` pointing to a provider-controlled hostname. The provider places the actual TXT record there. Enables fully automated renewal without any further DNS changes.

```json
{
  "providerId": "appplatform.example",
  "providerName": "Acme AppPlatform",
  "serviceId": "custom-domain-ssl-cname",
  "serviceName": "Acme AppPlatform Custom Domain with SSL (CNAME delegation)",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.appplatform.example",
  "syncRedirectDomain": "dashboard.appplatform.example",
  "hostRequired": true,
  "description": "Points a subdomain to your Acme AppPlatform deployment and sets up permanent ACME CNAME delegation for automated certificate renewal.",
  "records": [
    {
      "groupId": "cname",
      "type": "CNAME",
      "host": "@",
      "pointsTo": "%cnameTarget%",
      "ttl": 600
    },
    {
      "groupId": "acme",
      "type": "CNAME",
      "host": "_acme-challenge.%domain%.",
      "pointsTo": "%acmeCnameDelegation%",
      "ttl": 600
    }
  ]
}
```

---

## Explanation of Key Template Setup

### `hostRequired: true` and the `@` / `%domain%.` distinction

This template uses `hostRequired: true`, meaning the Domain Connect flow requires a `host` parameter specifying which subdomain is being connected (e.g. `app`, `shop`, `blog`). Within the template, `@` resolves to that user-supplied subdomain — so `"host": "@"` creates a record at `app.yourdomain.com` when the user specifies `app`.

The ACME challenge record must be placed at `_acme-challenge.app.yourdomain.com` — but it cannot use `@` as a prefix, because `@` would expand to `_acme-challenge.app.yourdomain.com` only if the host were `_acme-challenge.app`. The correct approach uses the built-in `%domain%.` variable:

```
"host": "_acme-challenge.%domain%."
```

`%domain%` always resolves to the **zone apex** (`yourdomain.com`) regardless of the `host` apply parameter. The trailing dot makes it an absolute DNS name, anchoring it to the apex and preventing any relative-name ambiguity. So for a user connecting `app.yourdomain.com`:

- `"host": "@"` → `app.yourdomain.com` (the hosting CNAME)
- `"host": "_acme-challenge.%domain%."` → `_acme-challenge.yourdomain.com`

### ACME challenge TXT — direct placement

The `%acmeChallenge%` variable is the Base64url-encoded key authorisation token generated by your ACME client for this specific certificate request. It is injected when the template is applied. The TTL of 300 seconds is intentionally short — the TXT record is only needed during validation and can be removed or replaced for the next renewal.

**Limitation:** the TXT value is valid only for one certificate issuance. For renewal, the template must be re-applied with a new `%acmeChallenge%` value — which requires a new Domain Connect consent flow, or the use of the async flow to push the update without user interaction.

### ACME CNAME delegation — the preferred pattern

Instead of placing the TXT value directly, the `acme` group places a CNAME:

```
_acme-challenge.yourdomain.com  CNAME  <token>.acme.appplatform.example
```

The provider controls `<token>.acme.appplatform.example` and places the TXT record there. The ACME CA follows the CNAME and validates against the provider's TXT. This is the [acme-dns](https://github.com/joohoi/acme-dns) pattern, standardised in [RFC 8555](https://datatracker.ietf.org/doc/html/rfc8555) and supported by all major ACME CAs.

Benefits:
- **Permanent setup:** the CNAME is created once and never needs to change
- **Fully automated renewal:** the provider rotates the TXT record on its own infrastructure for every renewal, with no DNS change on the user's domain
- **No token exposure:** the user never sees or approves a cryptographic token — just "create a CNAME for certificate validation"

The `%acmeCnameDelegation%` variable in the example is a per-customer hostname on the provider's infrastructure (e.g. `a1b2c3d4.acme.appplatform.example`).

### TTL choices

- CNAME for hosting: 600s — allows rapid redeployment
- ACME TXT (direct): 300s — short-lived by nature; faster expiry aids cleanup
- ACME CNAME delegation: 600s — semi-permanent; should persist for the life of the deployment

---

## Template Examples in the Public Repository

- [vercel.com / website](https://github.com/domain-connect/Templates/blob/master/vercel.com.website.json) — includes separate TXT verification groups alongside CNAME and apex groups; shows the pattern of combining hosting and validation records in one template
- [tinkerhost.net / th-sslverify](https://github.com/domain-connect/Templates/blob/master/tinkerhost.net.th-sslverify.json) — dedicated SSL verification template using a TXT record for DV validation alongside hosting records
- [buckt.dev / acm-validation](https://github.com/domain-connect/Templates/blob/master/buckt.dev.acm-validation.json) — ACM (AWS Certificate Manager) DNS validation template: TXT record for certificate validation placed separately from the hosting CNAME

---

## Things to Take Care About

**CNAME at `_acme-challenge` and ACME CA support.**  
All major ACME CAs (Let's Encrypt, ZeroSSL, Google Trust Services) follow CNAMEs when resolving `_acme-challenge` records. This is specified behaviour per RFC 8555. However, some private or enterprise CAs do not follow CNAMEs. Verify your CA supports CNAME delegation before choosing the delegation pattern.

**The direct TXT pattern requires re-consent for renewal.**  
If you place the ACME TXT value directly in the template, certificate renewal requires placing a new TXT value — which means either re-running the Domain Connect consent flow (unacceptable for automated renewal) or having async flow write access to push the update. If your platform does not hold an async token for the user's DNS provider, use the CNAME delegation pattern instead.

**`_acme-challenge` TXT conflicts.**  
If the user already has an `_acme-challenge` TXT record (from a previous CA validation or a different platform), the DNS provider's conflict handling will determine whether it is replaced or whether both records coexist. Multiple TXT records at `_acme-challenge` are valid DNS — ACME CAs check all of them. This is generally harmless, but stale tokens from previous issuances can accumulate. Include `"txtConflictMatchingMode": "None"` if you want the DNS provider to leave existing TXT records in place, or rely on default conflict handling to replace them.

---

## Specificities and Remarks

- **ACME DNS-01 vs HTTP-01 for custom domains.** HTTP-01 requires the platform to serve the challenge token at `http://<domain>/.well-known/acme-challenge/<token>`. This only works after the CNAME is propagated and traffic is reaching the platform — creating a race condition during initial setup. DNS-01 is immune to this race: the TXT record can be validated before any HTTP traffic flows. For custom domain provisioning, DNS-01 is the more reliable choice.
- **The `%domain%.` trailing dot.** The trailing dot on `%domain%.` is significant in DNS: it denotes an absolute (fully qualified) name. Without it, some DNS providers interpret the host as relative to the current zone and append the zone name again. Always include the trailing dot when using `%domain%` in a `host` field to construct an absolute name.
- **Combining this template with async flow for renewal.** If your platform holds an async OAuth token for the user's DNS provider (established during onboarding), it can push ACME TXT updates directly via the Domain Connect async apply endpoint — without requiring the user to re-approve. This makes the direct TXT pattern viable for renewal, eliminating the need for CNAME delegation. The async token approach requires the DNS provider to support the async flow and issue long-lived or refreshable tokens (see [UC-08](./UC-08_Dynamic_DNS.md) for token lifecycle details).
- **Separate `serviceId` from the plain subdomain template.** This template should have a different `serviceId` than the basic subdomain hosting template (UC-05). This allows DNS providers to advertise support for SSL provisioning independently of basic CNAME hosting, and allows your service to select the appropriate template based on what the target DNS provider supports.
