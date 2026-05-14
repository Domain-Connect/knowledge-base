# UC-07: URL Redirect

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**DNS records used:** A, AAAA (redirect service IPs); optionally REDIR301 / REDIR302  
**Complexity:** Very Low

---

## Use Case Description

A service provider operates a redirect infrastructure: when a browser requests `yourdomain.com`, the redirect service intercepts the HTTP request and issues a 301 or 302 redirect to a destination URL. The domain's DNS A record (and AAAA for IPv6) points to the redirect service's IP. The redirect service is responsible for the HTTP-layer forwarding; DNS only delivers the browser to the right server.

This is structurally identical to website hosting at the DNS level — an A record at the apex. What distinguishes it as a use case is:
- The "content" served is a redirect, not actual website content
- The user's intent is forwarding traffic, not hosting anything
- The destination URL is often user-configurable and unrelated to the domain being configured
- Path-forwarding and URL masking variants add complexity

Typical products in this category:
- Domain redirect services (park a domain, forward it to another URL)
- URL shortener platforms with custom domains
- Brand link management services
- Campaign tracking link platforms

---

## Value Added for the End User

Domain redirect setup is deceptively simple (it is "just an A record") but reliably fails in practice. Users set the A record, forget to also set `www`, forget AAAA, or point to the wrong IP because they copied it from a help article for a different service tier. The result is a redirect that works from some browsers but not others, or that works at `www.yourdomain.com` but not `yourdomain.com`.

With a Domain Connect template, both A and AAAA are set correctly and atomically. A `www` CNAME can be included in the same template. The user's only task is approving the consent screen.

Key benefits:
- Correct A + AAAA + www CNAME in one step, eliminating partial-redirect configurations
- Provider controls the redirect IP — no risk of the user copying an outdated IP from a help article
- Propagation is immediate from the DNS provider side; no waiting for propagation to "take effect" on the redirect service

---

## Example Template

```json
{
  "providerId": "linkforward.example",
  "providerName": "Acme LinkForward",
  "serviceId": "domain-redirect",
  "serviceName": "Acme LinkForward Domain Redirect",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.linkforward.example",
  "syncRedirectDomain": "app.linkforward.example",
  "description": "Points your domain to Acme LinkForward for HTTP redirect to your destination URL.",
  "records": [
    {
      "groupId": "redirect",
      "type": "A",
      "host": "@",
      "pointsTo": "%ipv4%",
      "ttl": 3600
    },
    {
      "groupId": "redirect",
      "type": "AAAA",
      "host": "@",
      "pointsTo": "%ipv6%",
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

### A and AAAA with variable IPs

The redirect service's IPs are injected as variables. This is appropriate when:
- Different service tiers use different IPs
- The user's redirect configuration is hosted on a specific server or cluster
- The provider needs the flexibility to reassign IPs without a code change to the template

If your redirect service uses a single, stable anycast IP for all customers, hardcoded IPs simplify the template and eliminate any risk of variable injection errors:

```json
{
  "type": "A",
  "host": "@",
  "pointsTo": "203.0.113.201",
  "ttl": 3600
}
```

### CNAME `www → @`

Without this record, `www.yourdomain.com` does not reach the redirect service — users arriving with `www.` in the URL get a DNS lookup failure instead of the redirect. Including it in the same `groupId` as the A record ensures both paths are always configured together.

### REDIR301 / REDIR302 record types

Some DNS providers that implement Domain Connect support `REDIR301` and `REDIR302` as native record types. These encode the redirect destination URL directly in DNS, and the DNS provider's own infrastructure performs the HTTP redirect — no separate redirect service required.

```json
{
  "type": "REDIR301",
  "host": "@",
  "target": "%destinationUrl%",
  "ttl": 3600
}
```

This pattern is only supported by DNS providers that have implemented these extended record types. It is not universally available. Before building a redirect product on `REDIR301`/`REDIR302`, verify that the DNS providers you target support them. A plain A-record approach (pointing to your own redirect service) is more portable.

---

## Template Examples in the Public Repository

- [redirect.pizza / apex](https://github.com/domain-connect/Templates/blob/master/redirect.pizza.apex.json) — minimal: A + AAAA at apex with variable IPs (`%ipv4%`, `%ipv6%`); no www CNAME (handled in a separate template)
- [redirect.pizza / apex-www](https://github.com/domain-connect/Templates/blob/master/redirect.pizza.apex-www.json) — extends the apex template with a www CNAME; shows the split-template approach where www and apex can be configured independently

---

## Things to Take Care About

**No content at the redirect IP means search engines index nothing.**  
A redirect domain that was previously indexed will lose its search ranking during the transition. This is expected and by design for redirect-only domains, but worth mentioning in your user documentation — particularly for users who are forwarding from a previously ranked domain.

**URL masking (frame redirect) is an SEO anti-pattern.**  
Some redirect services offer "URL masking" (loading the destination inside an iframe while keeping the original URL in the browser bar). This is a legitimate use case for certain applications but is widely considered an SEO and accessibility anti-pattern. Domain Connect does not distinguish between redirect types — the HTTP behaviour is entirely your service's concern.

**HTTPS redirect requires a valid TLS certificate at your redirect IP.**  
When the user's domain resolves to your redirect IP and a browser requests `https://yourdomain.com`, your server must present a valid certificate for `yourdomain.com`. This requires ACME / Let's Encrypt provisioning at the point the A record is set. Plan for the propagation delay between the Domain Connect callback and the moment DNS is globally live.

**The redirect destination URL is not a DNS concern.**  
The template sets the DNS side only. The redirect destination (`https://example.com/landing`) must be configured separately in your platform. Domain Connect passes variables to the template, but multi-step configuration (DNS record + redirect rule in your service) must be orchestrated by your backend after the template is applied. Use the Domain Connect async flow callback to trigger redirect rule creation.

**Wildcard subdomains for redirect are not covered by this template.**  
If you need to redirect all subdomains (`*.yourdomain.com` → destination), that requires a wildcard A record, which Domain Connect does not natively support. Handle wildcard setups via your DNS provider's native interface or provide guidance to users alongside the Domain Connect flow.

---

## Specificities and Remarks

- **Split apex / www templates** (as in the redirect.pizza examples) allow users to configure apex and www redirects independently — useful when different destinations are intended for `yourdomain.com` vs `www.yourdomain.com`. Each template is a separate `serviceId`; they can be applied sequentially via the same OAuth flow if your service chains them.
- **Path-preserving redirects.** A 301 redirect from `yourdomain.com` to `otherdomain.com` sends all traffic to the destination root. A path-preserving redirect forwards `yourdomain.com/path/page` to `otherdomain.com/path/page`. This is purely HTTP-layer behaviour and does not affect the DNS template.
- **`multiInstance: false` (default).** A domain should only have one redirect configured. There is no valid use case for multiple redirect templates on the same domain. Leave `multiInstance` at its default (false).
- **TTL choice for redirect IPs.** A TTL of 3600 (1 hour) is standard. Shorter TTLs (600s) are appropriate if you rotate IPs frequently. Very short TTLs (60s or less) increase DNS query load and are unnecessary for redirect infrastructure that changes rarely.
