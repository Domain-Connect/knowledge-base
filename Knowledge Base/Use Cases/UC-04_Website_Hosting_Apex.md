# UC-04: Website Hosting — Apex Domain

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**DNS records used:** A, AAAA, CNAME (www), APEXCNAME, REDIR301  
**Complexity:** Low–Medium

---

## Use Case Description

A service provider hosts a website and the user wants to point their domain's root (apex) to that hosting — `yourdomain.com` rather than `www.yourdomain.com`. This requires an A record (and optionally AAAA for IPv6) at `@` (the apex), plus a CNAME for `www` to redirect www-prefixed traffic to the same destination.

This is the most frequently used template pattern for website builders, e-commerce platforms, CMS hosts, and app deployment platforms that support apex domains. It is structurally simple — often just two or three records — but carries the highest operational risk of any template type, because replacing the A record at `@` immediately changes where the domain resolves for all HTTP traffic.

Typical products in this category:
- Website builders and landing page tools
- E-commerce platforms (shop on `yourdomain.com`)
- CMS hosting platforms (WordPress, Ghost, static sites)
- App deployment platforms with anycast IPs
- Portfolio and personal site platforms

---

## Value Added for the End User

Connecting a domain to a website builder is the most common Domain Connect deployment scenario. Users expect a "connect domain" button; when they click it, they want it to work. Manual A-record configuration requires the user to find the correct IP address, navigate the DNS panel, identify and delete any conflicting A records, and wait for propagation — a 15–30 minute process with numerous drop-off points.

With a Domain Connect template, the user is redirected to their DNS provider's consent screen that shows exactly which records will be changed, clicks Approve, and the domain is live within the TTL window. The provider handles conflict resolution (removing old A records), dual-stack setup (A + AAAA), and the www CNAME in one atomic operation.

Key benefits:
- Fastest DNS change a user can make — 3 records, one click
- DNS providers handle conflict resolution: old conflicting A records are removed
- IPv6 (AAAA) can be added alongside IPv4 without the user knowing it exists
- The www CNAME ensures `www.yourdomain.com` works correctly without a separate manual step

---

## Example Template

```json
{
  "providerId": "sitehoster.example",
  "providerName": "Acme Sites",
  "serviceId": "website-hosting",
  "serviceName": "Acme Sites Website Hosting",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.sitehoster.example",
  "syncRedirectDomain": "app.sitehoster.example",
  "description": "Points your domain to your Acme Sites website.",
  "records": [
    {
      "groupId": "apex",
      "type": "A",
      "host": "@",
      "pointsTo": "203.0.113.42",
      "ttl": 3600
    },
    {
      "groupId": "apex",
      "type": "AAAA",
      "host": "@",
      "pointsTo": "2001:db8::42",
      "ttl": 3600
    },
    {
      "groupId": "www",
      "type": "CNAME",
      "host": "www",
      "pointsTo": "@",
      "ttl": 3600
    }
  ]
}
```

---

## Explanation of Key Template Setup

### A record at `@` — fixed IP

The A record points the apex domain to your hosting infrastructure's IP address. When the IP is the same for all customers (a shared anycast or load-balancer address), it is a fixed value in the template. When the IP is customer-specific (dedicated hosting, per-tenant infrastructure), use a variable: `"pointsTo": "%ipv4%"`.

Fixed IPs are simpler and more robust. They require no runtime variable injection and the template is self-contained. If your infrastructure uses multiple IPs (round-robin), include one A record per IP, all in the same `groupId`.

### AAAA record — IPv6 alongside IPv4

Adding an AAAA record at `@` enables IPv6 connectivity. This is invisible to users but matters for reachability from IPv6-only networks (growing in mobile and enterprise contexts) and improves Google Search ranking on some metrics. If your infrastructure supports IPv6, include the AAAA record. If not, omit it — do not add a placeholder that resolves to an unresponsive address.

### CNAME for `www` pointing to `@`

`"pointsTo": "@"` is a shorthand that most DNS providers translate to the apex domain itself — effectively making `www.yourdomain.com` resolve to the same A record as `yourdomain.com`. This avoids the need to duplicate the IP in the CNAME target and means the www record stays in sync if the apex A record is ever updated.

### Conflict resolution

When this template is applied, the DNS provider will remove any existing A/AAAA records at `@` that conflict. This is intentional and correct behaviour — the user is replacing their current hosting destination. However, it is also the most consequential change Domain Connect can make: existing hosted content stops being served immediately. Ensure your UI makes this clear before the user initiates the flow.

### Variable IP variant

For per-customer IP addresses:

```json
{
  "groupId": "apex",
  "type": "A",
  "host": "@",
  "pointsTo": "%ipv4%",
  "ttl": 3600
}
```

The IP is injected by the service when constructing the Domain Connect URL or signed query. Validate the IP on your backend before passing it as a template variable — never allow user-supplied IPs to flow into the template without validation.

---

## Template Examples in the Public Repository

- [shopify.com / website](https://github.com/domain-connect/Templates/blob/master/shopify.com.website.json) — A + AAAA at apex + CNAME for www + an additional CNAME for per-customer verification; hardcoded anycast IPs
- [wordpress.com / hosting](https://github.com/domain-connect/Templates/blob/master/wordpress.com.hosting.json) — two A records (redundant IPs) + CNAME www → @, all in one `mapping` groupId
- [vercel.com / website](https://github.com/domain-connect/Templates/blob/master/vercel.com.website.json) — flexible multi-group template supporting apex via A record, apex via APEXCNAME, or subdomain via CNAME, with TXT verification groups; uses `hostRequired: true`

---

## When Your Platform Cannot Provide a Stable IP

Many modern hosting platforms — CDN-backed deployments, serverless platforms, multi-tenant PaaS — do not assign stable, dedicated IP addresses. Their infrastructure is identified by a hostname (e.g. `myproject.acmesites.example`), and the IPs behind that hostname change as the platform scales or rebalances. In those cases, the natural DNS integration is a CNAME — but a CNAME at the apex is prohibited by DNS standards (RFC 1034). This is the fundamental tension in apex domain hosting.

Three approaches exist within the Domain Connect ecosystem, each with different trade-offs in terms of DNS provider support and user experience. If you need to support multiple approaches, **define each as a separate template** with its own `serviceId` — this allows DNS providers to advertise which templates they support, and your service can discover at runtime which approach is available for a given user's DNS provider.

### Approach 1: CNAME flattening (APEXCNAME)

Some DNS providers implement CNAME-like behaviour at the apex by resolving the CNAME target at query time and returning the resulting A record(s) to the client. This is known as CNAME flattening, ALIAS, or ANAME depending on the provider. Domain Connect exposes this as the `APEXCNAME` record type.

A template using `APEXCNAME` looks identical to a subdomain CNAME template (see [UC-05](./UC-05_Website_Hosting_Subdomain.md)), with the difference that `host` is `@` and the type is `APEXCNAME`:

```json
{
  "providerId": "sitehoster.example",
  "providerName": "Acme Sites",
  "serviceId": "website-hosting-cname",
  "serviceName": "Acme Sites Website Hosting (CNAME)",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.sitehoster.example",
  "syncRedirectDomain": "app.sitehoster.example",
  "hostRequired": true,
  "description": "Points your domain to your Acme Sites website using CNAME flattening.",
  "records": [
    {
      "groupId": "apex",
      "type": "APEXCNAME",
      "host": "@",
      "pointsTo": "%cnameTarget%",
      "ttl": 600
    },
    {
      "groupId": "www",
      "type": "CNAME",
      "host": "www",
      "pointsTo": "@",
      "ttl": 600
    }
  ]
}
```

**When the DNS provider supports `APEXCNAME`**, it also interprets a subdomain-style CNAME template (`hostRequired: true`, `type: CNAME`, `host: "@"`) as an apex CNAME — meaning the same template used for subdomain hosting (UC-05) can work for the apex without a separate template. This is provider-specific behaviour: the provider recognises that `@` with `hostRequired` refers to the apex context and applies CNAME flattening accordingly.

**Limitation:** `APEXCNAME` is not universally supported. DNS providers that do not implement CNAME flattening will reject or ignore this record type. Do not rely on it as your only integration path.

### Approach 2: Apex-to-www redirect via REDIR record

Some DNS providers support `REDIR301` and `REDIR302` record types that perform an HTTP redirect at the DNS level — the provider's own infrastructure serves the redirect response. A common use of this is redirecting `yourdomain.com` to `www.yourdomain.com`, where `www` can then be a standard CNAME to the hosting platform.

```json
{
  "providerId": "sitehoster.example",
  "providerName": "Acme Sites",
  "serviceId": "website-hosting-redirect",
  "serviceName": "Acme Sites Website Hosting (www redirect)",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.sitehoster.example",
  "syncRedirectDomain": "app.sitehoster.example",
  "description": "Redirects your apex domain to www, then points www to your Acme Sites website.",
  "records": [
    {
      "groupId": "apex-redirect",
      "type": "REDIR301",
      "host": "@",
      "target": "https://www.%fqdn%",
      "ttl": 3600
    },
    {
      "groupId": "www",
      "type": "CNAME",
      "host": "www",
      "pointsTo": "%cnameTarget%",
      "ttl": 600
    }
  ]
}
```

This approach keeps the hosting integration as a pure CNAME (on `www`) while using the DNS provider's own redirect infrastructure to handle the apex. No stable IP required.

**Limitation:** `REDIR301`/`REDIR302` are even less widely supported than `APEXCNAME`. A DNS provider that supports neither means this approach is unavailable for that user.

### Approach 3: Own or external redirect service with a stable IP

The most portable approach — and the fallback when neither APEXCNAME nor REDIR records are available — is to point the apex A record at a redirect service that issues an HTTP 301 to the `www` subdomain (or any other target). The redirect service has a stable, dedicated IP. The `www` CNAME then points to the hosting platform.

This is effectively a combination of UC-04 (apex A record) and the redirect-service pattern from [UC-07](./UC-07_URL_Redirect.md):

```json
{
  "providerId": "sitehoster.example",
  "providerName": "Acme Sites",
  "serviceId": "website-hosting-apex-redirect",
  "serviceName": "Acme Sites Website Hosting (apex via redirect)",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.sitehoster.example",
  "syncRedirectDomain": "app.sitehoster.example",
  "description": "Points your apex domain to Acme Sites' redirect service, which forwards to www. Points www to your Acme Sites website.",
  "records": [
    {
      "groupId": "apex",
      "type": "A",
      "host": "@",
      "pointsTo": "203.0.113.99",
      "ttl": 3600
    },
    {
      "groupId": "www",
      "type": "CNAME",
      "host": "www",
      "pointsTo": "%cnameTarget%",
      "ttl": 600
    }
  ]
}
```

The IP `203.0.113.99` is your redirect service — a stable, dedicated address that serves only HTTP 301s from `yourdomain.com` to `www.yourdomain.com`. Your hosting platform's actual IPs are hidden behind the `www` CNAME and can change at any time.

**This approach works with every DNS provider** — it only uses A and CNAME records. It is the universal fallback.

**Limitation:** You must operate (or integrate with) a redirect service with a stable IP. You also introduce an extra HTTP hop for every apex request. For most use cases this is acceptable — browsers follow the redirect quickly and it only affects the apex, not `www`.

### Summary: when to use which approach

| Approach | DNS provider support | IP required | Extra hop |
|----------|---------------------|-------------|-----------|
| `APEXCNAME` / CNAME flattening | Limited | No | No |
| `REDIR301` at apex | Limited | No | Yes (HTTP) |
| A record → redirect service | Universal | Yes (stable) | Yes (HTTP) |
| A record → hosting IP (UC-04 baseline) | Universal | Yes (stable hosting IP) | No |

If your platform needs to work across all DNS providers, implement the redirect-service approach as the baseline template and offer `APEXCNAME` as a separate, optional template for providers that support it. Discovery of which templates a DNS provider supports is part of the Domain Connect provider metadata — your service can select the best available approach automatically.

---

## Things to Take Care About

**Replacing an active A record takes down existing content immediately.**  

If the user's domain currently points to another website, applying this template replaces that immediately. The consent screen should name the current IP if possible, and your UI should warn the user that this change is immediate and will replace existing content.

**Do not hardcode IPs you do not control long-term.**  

If your infrastructure IPs change (CDN provider migration, IP address reassignment), all domains pointed to the old IP break simultaneously and silently. If you operate on a shared anycast range that is stable, hardcoded IPs are fine. Otherwise, use per-customer variables or CNAME-based hosting (see [UC-05](./UC-05_Website_Hosting_Subdomain.md)) where a CNAME pointing to your platform gives you the ability to change the IP behind it without touching DNS.

**www CNAME conflicts with existing records.**  

If the user has existing records at `www` (e.g. a CNAME to a different host), the DNS provider will remove them. This is expected but should be communicated.

**IPv4-only infrastructure with AAAA record in template.**  

If you include an AAAA record but your servers do not handle IPv6 traffic, connections from IPv6-only clients will time out. Only include AAAA if your infrastructure genuinely responds on the IPv6 address.

---

## Specificities and Remarks

- **`hostRequired: true`** is appropriate when your platform requires the user to specify a subdomain as part of the domain-connect flow (e.g. a multi-tenant platform where each tenant has a path-based host identifier). For standard apex hosting, `hostRequired` is not needed.
- **Verification records alongside hosting records.** Several real-world templates (e.g. Shopify) include a CNAME at a per-customer verification subdomain alongside the A record. This allows the platform to confirm that the domain is correctly pointed before activating the site. This is a clean pattern — include the verification record in its own `groupId` so it is clearly presented as a separate item in the consent screen.
- **Multiple A records for round-robin.** If your platform load-balances across multiple IPs, list each IP as a separate A record (all with the same `host: "@"` and the same `groupId`). The DNS provider will create all of them.
- **HTTPS certificate issuance.** Domain Connect does not handle TLS certificate provisioning. After the DNS change, your platform typically initiates certificate issuance (Let's Encrypt / ACME). Make sure your platform's certificate provisioning can tolerate the DNS propagation delay — do not assume records are globally live immediately after the template is applied.
