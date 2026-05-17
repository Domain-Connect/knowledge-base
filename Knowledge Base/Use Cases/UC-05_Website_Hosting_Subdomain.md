# UC-05: Website Hosting — Subdomain / CNAME

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**DNS records used:** CNAME (subdomain or apex-alias), TXT (optional verification)  
**Complexity:** Low

---

## Use Case Description

A service provider hosts a website, app, or service endpoint and the user wants to reach it at a subdomain of their own domain — `app.yourdomain.com`, `www.yourdomain.com`, `shop.yourdomain.com`, or similar. The template creates a CNAME pointing the user-specified (or fixed) subdomain to the provider's hosting infrastructure.

This is the simplest and most portable hosting pattern. Because a CNAME points to a hostname rather than an IP, the provider can change its infrastructure IP, move to a CDN, or rebalance traffic without requiring any DNS change from the user. It is also the foundation for nearly every SaaS "custom domain" feature.

Typical products in this category:
- SaaS platforms with custom domain features (help centres, portals, dashboards)
- App deployment platforms (JAMstack, serverless, container hosting)
- Landing page and funnel builders
- Community platforms, forums, and documentation sites
- Online stores hosted on a subdomain of an existing brand domain

---

## Value Added for the End User

Custom domain support in SaaS is a table-stakes feature, but CNAME setup has a surprisingly high failure rate. Users must identify the correct subdomain, find the CNAME target, and navigate their DNS panel — and a single typo in either field breaks everything. Verifying that the CNAME propagated correctly adds another layer of friction.

With a Domain Connect template, the CNAME target is provided by the platform and injected as a template variable. The user does not need to copy any string. The DNS provider creates the record atomically and the platform can immediately check resolution.

Key benefits:
- Eliminates copy-paste errors in CNAME targets (the most common cause of failed custom domain setups)
- The provider controls the CNAME target — IP changes and CDN migrations are transparent to the user
- Optional TXT verification record can be included in the same flow, removing a separate "verify domain" step
- Works for any subdomain, including `www`, `app`, `blog`, `shop`, `docs`, etc.

---

## Example Template

```json
{
  "providerId": "appplatform.example",
  "providerName": "Acme AppPlatform",
  "serviceId": "custom-domain",
  "serviceName": "Acme AppPlatform Custom Domain",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.appplatform.example",
  "syncRedirectDomain": "dashboard.appplatform.example",
  "hostRequired": true,
  "description": "Points a subdomain of your domain to your Acme AppPlatform deployment.",
  "records": [
    {
      "groupId": "cname",
      "type": "CNAME",
      "host": "@",
      "pointsTo": "%cnameTarget%",
      "ttl": 600
    },
    {
      "groupId": "verification",
      "type": "TXT",
      "host": "_acme-verify",
      "data": "acme-verify=%verificationToken%",
      "ttl": 600
    }
  ]
}
```

**Note on `host: "@"`:** When `hostRequired: true`, the `@` in `host` resolves to the user-supplied subdomain — not to the apex. So if the user specifies `app` as the host during the Domain Connect flow, the template creates `app.yourdomain.com CNAME %cnameTarget%`.

---

## Explanation of Key Template Setup

### `hostRequired: true` — user-specified subdomain

Setting `hostRequired: true` means the Domain Connect flow requires the user (or the initiating service) to supply a `host` parameter when constructing the URL. This host is substituted for `@` in all record definitions. This is the correct pattern when:

- Your platform assigns a subdomain per project, deployment, or tenant
- The user picks their preferred subdomain (`blog`, `shop`, `app`, etc.)
- The same template is reused across many different subdomain names

When `hostRequired: false` (the default), the `@` in `host` refers to the root of the domain. This is appropriate when your template always applies to the apex or to a fixed subdomain (e.g. always `www`).

### CNAME target as a variable

`%cnameTarget%` is injected by the platform when constructing the Domain Connect URL. The value is typically something like `projectname.appplatform.example` or a CDN-edge hostname. The user never sees or types this value — they just approve the consent screen that says "Create CNAME `app.yourdomain.com` → `projectname.appplatform.example`".

### Low TTL

The TTL of `600` seconds (10 minutes) is appropriate for CNAMEs in a deployment/hosting context. If a project is redeployed to a different hostname, the old CNAME needs to update quickly. For stable, long-lived deployments, `3600` is fine; for ephemeral or frequently changing environments, use `300`–`600`.

### Verification TXT record

Including a TXT record for domain ownership verification in the same template eliminates a separate "verify your domain" step. The platform can check for the TXT record after the template is applied to confirm the user owns the domain. Using a fixed subdomain like `_acme-verify` (chosen to avoid conflicts with real ACME challenges) keeps verification separate from the CNAME.

### Fixed subdomain variant

If your platform always uses a specific subdomain (e.g. always `www`), use `hostRequired: false` and hardcode the subdomain in `host`:

```json
{
  "groupId": "cname",
  "type": "CNAME",
  "host": "www",
  "pointsTo": "%cnameTarget%",
  "ttl": 3600
}
```

---

## Template Examples in the Public Repository

- [framer.com / subdomain](https://github.com/domain-connect/Templates/blob/master/framer.com.subdomain.json) — single CNAME with `hostRequired: true`; target uses a `%prefix%` variable to construct the Framer project hostname
- [vercel.com / website](https://github.com/domain-connect/Templates/blob/master/vercel.com.website.json) — multi-group template with separate groups for subdomain CNAME, apex A record, and apex CNAME (APEXCNAME), plus TXT verification groups; `hostRequired: true`
- [wpengine.com / cname-cdn](https://github.com/domain-connect/Templates/blob/master/wpengine.com.cname-cdn.json) — minimal CNAME with `hostRequired: true`; single record pointing `@` to the CDN hostname variable

---

## Things to Take Care About

**CNAME at apex (`@`) without `hostRequired` breaks the domain.**  

A CNAME at the root of a domain (the apex) is technically prohibited by DNS standards (RFC 1034) and breaks MX, NS, and other essential records. If you set `host: "@"` with `hostRequired: false`, the DNS provider may create an invalid CNAME at the apex. Always use `hostRequired: true` when using `@` as the host, or use `APEXCNAME` (see below) if you genuinely need apex support.

**APEXCNAME — apex CNAME support.**  

Some DNS providers implement a Domain Connect record type called `APEXCNAME` (or an `ALIAS`/`ANAME` record underneath). If your platform's target is a hostname (not an IP) and you need apex domain support, use `APEXCNAME` instead of `A`. Not all DNS providers support `APEXCNAME`, so either test against your target providers or provide both an `A`-record group and an `APEXCNAME` group, with the provider applying whichever it supports.

**`multiInstance: true` for multiple deployments.**  

If your platform allows a single domain to host multiple projects (e.g. `app.yourdomain.com` and `shop.yourdomain.com`), set `"multiInstance": true`. Without it, applying the template a second time may be treated as a conflict or an attempt to replace the first deployment.

**CNAME coexistence with other records.**  

A CNAME must be the only record at its name — DNS prohibits combining a CNAME with A, MX, or TXT records at the same subdomain. If the user already has records at the subdomain you are targeting, the DNS provider will need to remove them before creating the CNAME. Document which subdomains your template claims.

**Wildcard subdomains.**  

Domain Connect does not natively support wildcard CNAME records (`*`). If your platform needs a wildcard subdomain pointing to your infrastructure, this must be handled outside Domain Connect or via a separate template that uses a specific, well-known subdomain.

---

## Specificities and Remarks

- **Deployment verification via CNAME resolution.** After the template is applied, your platform can confirm the CNAME is correctly set by resolving the subdomain and verifying it reaches your infrastructure. This should happen automatically as part of your onboarding flow — do not ask the user to "check back in 24 hours".
- **HTTPS certificate issuance.** After the CNAME is in place, your platform will typically issue a TLS certificate for the subdomain. For ACME (Let's Encrypt), HTTP-01 or TLS-ALPN-01 challenges are typical; DNS-01 is less common for subdomain-only templates. Ensure your certificate provisioning pipeline is triggered immediately after the Domain Connect callback.
- **Short TTLs for transient deployments.** Preview environments, staging deployments, and temporary projects benefit from a TTL of 60–300 seconds. Long TTLs (3600+) are appropriate for production custom domains that won't change.
- **The `%fqdn%` built-in variable.** Domain Connect provides `%fqdn%` as a built-in variable (the full domain name being configured incl. host). You can use it to construct per-domain CNAME targets if your platform uses the user's domain as part of the target hostname — e.g. `"pointsTo": "%fqdn%.proxy.appplatform.example"`.
