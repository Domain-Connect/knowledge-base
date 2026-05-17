# UC-06: CDN, WAF & Reverse Proxy

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**DNS records used:** A (WAF/CDN IP), CNAME (www → @), CNAME (proxy subdomain)  
**Complexity:** Low–Medium

---

## Use Case Description

A service provider interposes its own network infrastructure between the domain and the user's origin server, typically for one or more of:

- **CDN (Content Delivery Network):** Caches and serves content from edge nodes close to end users
- **WAF (Web Application Firewall):** Inspects and filters HTTP traffic before it reaches the origin
- **Reverse proxy:** Terminates TLS, modifies headers, or routes requests to backend services

In all three cases, the DNS change is the same: the domain's A record (and CNAME for `www`) is pointed at the provider's infrastructure IP or hostname. Traffic then flows through the provider's network before reaching the origin server.

This pattern closely resembles [UC-04 (Website Hosting — Apex)](./UC-04_Website_Hosting_Apex.md) at the DNS level, but the intent and security implications differ: the origin server remains under the user's control, and the provider is a transparent intermediary rather than the content host. This distinction has implications for `warnPhishing`, record conflict handling, and how the consent screen is worded.

Typical products in this category:
- Cloud WAF and DDoS protection services
- CDN providers offering a one-click setup flow
- Reverse proxy services for performance optimisation
- Security-as-a-service platforms protecting web applications
- Edge computing platforms that proxy traffic to customer backends

---

## Value Added for the End User

Onboarding to a WAF or CDN traditionally requires the user to:
1. Find the provider's "activation IP" or CNAME target
2. Change the A record (or CNAME) in their DNS panel
3. Wait for propagation and confirm traffic is flowing through the provider
4. Optionally update `www` separately

Each step has a meaningful failure rate. Users often skip the `www` update, resulting in half their traffic bypassing the WAF. They point to the wrong IP because the provider has multiple IPs for different plans. They forget to update both A and AAAA records, leaving IPv6 traffic unprotected.

With a Domain Connect template, the provider injects the correct IP or CNAME target as a variable. The user approves a single consent screen. Both A and CNAME records are set atomically. No traffic path is accidentally left unprotected.

Key benefits:
- Atomic update of all traffic paths (A + AAAA + www CNAME)
- Provider controls the target IP — correct value is guaranteed
- Consent screen clearly names the provider, so the user understands what they are routing traffic through
- `warnPhishing` flag can be used to prompt the DNS provider to add a warning for this consequential change

---

## Example Template

```json
{
  "providerId": "edgeshield.example",
  "providerName": "Acme EdgeShield",
  "serviceId": "waf-proxy",
  "serviceName": "Acme EdgeShield Web Application Firewall",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.edgeshield.example",
  "syncRedirectDomain": "portal.edgeshield.example",
  "shared": true,
  "sharedProviderName": true,
  "warnPhishing": true,
  "description": "Routes your domain's web traffic through Acme EdgeShield for WAF protection and CDN acceleration.",
  "records": [
    {
      "groupId": "apex",
      "type": "A",
      "host": "@",
      "pointsTo": "%wafIp%",
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

### A record with variable IP

Unlike a pure website-hosting template where the IP is fixed and the same for all customers, WAF and CDN providers often assign per-customer or per-plan edge IPs. The `%wafIp%` variable is injected by the provider when constructing the Domain Connect URL or signed request. The provider's backend determines the correct IP based on the customer's account and plan.

If your platform uses a single anycast IP for all customers (common for WAF services), a fixed IP is fine and simpler: `"pointsTo": "203.0.113.100"`. No variable injection needed.

### `www` CNAME pointing to `@`

The `www` CNAME ensures that `www.yourdomain.com` also flows through the WAF/CDN. Without this, users who type `www.` in the browser access the origin server directly, bypassing all protection. This is one of the most common misconfiguration patterns when users set up WAF manually — the `@` record gets updated but `www` is forgotten.

### `shared: true` and `sharedProviderName: true`

These flags indicate that the template may be applied to a domain that already has another Domain Connect service from a different provider. Setting both to `true` allows the DNS provider to treat this as an "additive" or "replacing" operation rather than a conflict. This is appropriate for WAF/CDN providers because the user may already have a website-hosting template in place — the WAF intercepts traffic to the same origin.

In practice, applying a WAF template will replace the existing A record (which pointed to the origin). The `shared` flag signals to the DNS provider that this replacement is expected and intended.

### `warnPhishing: true`

A WAF/CDN/proxy template causes all HTTP traffic to flow through a third-party network. This is a significant trust action: the provider will see all requests and responses. DNS providers that support the `warnPhishing` flag will add an extra warning to the consent screen. This is appropriate here and builds user trust by making the scope of the change explicit.

### Per-customer CNAME variant

Some CDN providers use per-customer hostnames rather than IPs:

```json
{
  "groupId": "apex",
  "type": "APEXCNAME",
  "host": "@",
  "pointsTo": "%edgeHostname%",
  "ttl": 3600
}
```

`APEXCNAME` maps to the DNS provider's ALIAS or ANAME implementation. This enables the provider to change the underlying IP (e.g. scale edge nodes) without requiring the user to update DNS. Use `APEXCNAME` when your infrastructure target is a hostname; use `A` when it is an IP.

---

## Template Examples in the Public Repository

- [sucuri.net / waf](https://github.com/domain-connect/Templates/blob/master/sucuri.net.waf.json) — minimal WAF template: A record with a variable IP (`%ip%`) + CNAME `www → @`; uses `shared: true` and `sharedProviderName: true`
- [wpengine.com / cname-cdn](https://github.com/domain-connect/Templates/blob/master/wpengine.com.cname-cdn.json) — CDN CNAME with `hostRequired: true`; single CNAME pointing `@` (the user-specified host) to a variable CDN hostname

---

## Things to Take Care About

**Traffic interception is a high-trust action.**  

The consent screen wording matters. Users should understand they are routing traffic through a third party, not just changing a hosting IP. Use the `description` field to be explicit: "This redirects all web traffic for your domain through Acme EdgeShield's network." DNS providers surface this description in the consent UI.

**Origin server bypass via direct IP access.**  

A WAF/CDN only protects traffic that reaches it via DNS. If the origin server's IP is publicly known, attackers can bypass the WAF by sending requests directly to the IP. This is an application-layer concern, not a DNS concern — but it is worth flagging in your onboarding documentation.

**Avoid exposing the origin IP in the template.**  

The template should never contain the origin server IP — only the WAF/CDN IP. If a template variable is user-supplied and represents the origin, validate it server-side. A template that inadvertently exposes or logs origin IPs creates a security surface.

**IPv6 protection parity.**  

If your WAF/CDN infrastructure supports IPv6, include an AAAA record alongside the A record. An AAAA-only IPv6 path that bypasses your WAF is a protection gap.

**Template replacement vs. coexistence.**  

When a user already has a Domain Connect website-hosting template applied (e.g. pointing to a WordPress host), applying a WAF template replaces the A record. The website-hosting template is not automatically removed — the DNS provider applies the newer template on top. Ensure your platform's onboarding makes clear that the origin destination is now your WAF, and that the origin server should be updated to only accept traffic from your IP ranges.

---

## Specificities and Remarks

- **Reverse proxy for specific subdomains.** If your proxy only applies to one subdomain (e.g. `api.yourdomain.com`), use a CNAME template with `hostRequired: true` (see [UC-05](./UC-05_Website_Hosting_Subdomain.md)). The apex A-record pattern is only needed when proxying the root domain and `www`.
- **SSL termination.** When traffic is proxied through your infrastructure, TLS certificates are issued for the user's domain, not the origin. Your platform must provision a certificate for the user's domain. This is usually handled automatically but requires the DNS change (A record pointing to your infrastructure) to be in place first — a chicken-and-egg problem that Domain Connect solves by making the DNS change instant.
- **`syncBlock: true` is rarely appropriate here.** WAF and CDN onboarding benefits from the synchronous (OAuth-based) flow, where the DNS change and account activation happen in one session. `syncBlock: true` would restrict the template to async-only, which is a worse user experience.
- **Multiple A records for anycast.** If your WAF/CDN uses multiple anycast IPs for round-robin or geographic routing, include one A record per IP in the same `groupId`. The DNS provider will create all of them.
