# UC-08: Dynamic DNS

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**DNS records used:** A, AAAA (low TTL, updated by client)  
**Complexity:** Low–Medium

---

## Use Case Description

A client application (home router, IoT device, self-hosted server, home automation hub) automatically updates an A or AAAA record whenever the device's public IP address changes. The Domain Connect template establishes the initial record with the current IP; the DDNS client then uses the Domain Connect **async flow** to push updates autonomously — without any further user interaction.

This use case is unique in the Domain Connect ecosystem because the template is not a one-time configuration: it is the bootstrap step for an ongoing, automated relationship between a client and a DNS provider. The OAuth access token obtained during async flow setup is the credential the client uses for all future updates.

Typical products in this category:
- Home lab and self-hosted server connectivity
- IP camera and NVR remote access
- Home automation platforms (point a stable hostname at a residential connection)
- IoT devices that need a stable DNS name despite dynamic ISP-assigned IPs
- Personal VPN servers on consumer internet connections

---

## Value Added for the End User

Without Domain Connect, DDNS setup requires the user to:
1. Create a DNS record manually with their current IP in the DNS panel
2. Configure a DDNS client with DNS provider credentials (API key, account login)
3. Verify that the client is successfully pushing updates

Step 2 is where most users fail: each DNS provider has a different API, different credential format, and different update endpoint. DDNS client software either doesn't support the user's provider or requires provider-specific configuration that most users cannot navigate.

With Domain Connect, the initial record creation is handled by the template (step 1). The async OAuth flow (step 2) produces a standardised access token that works with any Domain Connect–compatible DNS provider. The DDNS client only needs to implement the Domain Connect async update call — one interface, all providers.

Key benefits:
- No DNS-panel credentials shared with the DDNS client — only a scoped OAuth token
- Token scope is limited to the specific template (only allowed to update this record type)
- The client can rotate IP updates as frequently as needed without re-authenticating
- IPv4 and IPv6 can be managed in separate groups, applied selectively per address family

---

## Example Template

```json
{
  "providerId": "dynhost.example",
  "providerName": "Acme DynHost",
  "serviceId": "dynamic-dns",
  "serviceName": "Acme DynHost Dynamic DNS",
  "version": 1,
  "syncBlock": true,
  "warnPhishing": true,
  "description": "Creates a dynamic DNS record for your domain, kept up to date by the Acme DynHost client.",
  "records": [
    {
      "groupId": "IPv4",
      "type": "A",
      "host": "@",
      "pointsTo": "%IPv4%",
      "ttl": "60"
    },
    {
      "groupId": "IPv6",
      "type": "AAAA",
      "host": "@",
      "pointsTo": "%IPv6%",
      "ttl": "60"
    }
  ]
}
```

---

## Explanation of Key Template Setup

### `syncBlock: true` — async-only flow

This is the most important field in a DDNS template. Setting `syncBlock: true` restricts the template to the **asynchronous flow only** and prevents it from being applied via the synchronous (one-shot OAuth) flow.

The reason: the synchronous flow executes a single DNS change and returns. It does not produce a persistent access token. If a user applied a DDNS template via the sync flow, the initial record would be created, but the DDNS client would have no credential to push future updates.

The async flow works differently: the DNS provider issues an OAuth access token (and typically a refresh token) scoped to the specific template. The DDNS client stores this token and calls the DNS provider's Domain Connect update endpoint each time the IP changes — indefinitely, without user involvement.

`syncBlock: true` guarantees every user goes through the async path. There is no other use case in the Domain Connect ecosystem where `syncBlock: true` is the correct default; DDNS is the canonical and essentially exclusive use case for this flag.

### Very low TTL — 60 seconds

A TTL of 60 seconds ensures that after the client pushes a new IP, resolvers worldwide stop using the old IP within ~60 seconds. This is the correct default for dynamic DNS.

Longer TTLs (e.g. 3600) mean IP changes take an hour to propagate — rendering the DDNS system nearly useless for real-time connectivity. The 60-second value in the example is a string (`"60"`), which is valid; the Domain Connect schema accepts both numeric and string TTL values.

Some DDNS platforms use even shorter TTLs (30s or less). Balance this against increased DNS query load on the provider.

### Separate groupIds per address family

IPv4 and IPv6 are in separate `groupId` blocks (`"IPv4"` and `"IPv6"`). This allows:
- An IPv4-only client to apply only the A record group
- A dual-stack client to apply both
- The DNS provider to handle partial application cleanly (e.g. skip AAAA if IPv6 is not supported)

This is the pattern used in the reference `dynamicdns-v2` template and should be followed for any new DDNS template.

### `warnPhishing: true`

A DDNS template grants a third-party client persistent write access to the A record at the domain's apex. This is a significant capability. Setting `warnPhishing: true` prompts DNS providers that support the flag to display an additional warning in the consent screen, making the scope of the permission clear to the user.

### No `syncPubKeyDomain` or `syncRedirectDomain`

Because the template is async-only (`syncBlock: true`), it does not need `syncPubKeyDomain` (used for synchronous URL signing) or `syncRedirectDomain` (used for OAuth redirect in synchronous flow). These fields are simply omitted.

---

## Template Examples in the Public Repository

- [domainconnect.org / dynamicdns-v2](https://github.com/domain-connect/Templates/blob/master/domainconnect.org.dynamicdns-v2.json) — canonical reference: A + AAAA with 60s TTL, `syncBlock: true`, separate IPv4/IPv6 groupIds
- [domainconnect.org / dynamicdns](https://github.com/domain-connect/Templates/blob/master/domainconnect.org.dynamicdns.json) — v1 reference: IPv4-only, single `%IP%` variable, simpler structure

---

## DNS Provider Requirements for DDNS Support

DDNS imposes requirements on the DNS provider that go beyond what is needed for any other Domain Connect use case. Before exposing DDNS support to end users, DNS providers must address two areas:

### Long-lived tokens or refresh token support

See "Things to Take Care About" below. This is a hard prerequisite — DDNS cannot function without it.

### OAuth client registration: public client or per-user registration

The Domain Connect async flow is an OAuth 2.0 authorisation code flow. Every OAuth flow requires a registered client — an entity with a `client_id` (and typically a `client_secret`) that the DNS provider's authorisation server recognises. For DDNS, the client is the DDNS software running on the user's device.

There are two practical approaches, each with trade-offs:

**Option 1: DNS provider registers a public OAuth client for DDNS use**

The DNS provider pre-registers a dedicated OAuth client for generic DDNS use and publishes the `client_id` openly. DDNS client software ships with this `client_id` hardcoded. No per-user registration is required. Any user of that DNS provider can use any compatible DDNS client immediately.

This is the user-friendliest model and is how the [DomainConnectDDNS](https://github.com/Domain-Connect/DomainConnectDDNS) reference client is designed to work. It uses the [PKCE extension (RFC 7636)](https://datatracker.ietf.org/doc/html/rfc7636) to protect the authorisation code without requiring a client secret — making it safe to use a public `client_id` even on devices where a secret cannot be stored securely.

Trade-off: the DNS provider loses the ability to revoke access for a specific DDNS client application without affecting all users of that `client_id`.

**Option 2: Each user (or DDNS operator) registers their own OAuth client**

The DNS provider requires each party deploying a DDNS solution to register an OAuth client in the provider's developer portal. The DDNS software is then configured with the user's own `client_id` and `client_secret`.

This gives the DNS provider full control and auditability. It is appropriate for enterprise or managed deployments. However, it adds a non-trivial configuration step for end users and makes generic DDNS clients (that cannot know the user's `client_id` in advance) impractical.

**Recommendation:** DNS providers supporting DDNS should register and publish at least one public OAuth client for DDNS use, using PKCE. This is what makes generic, open-source DDNS clients work out of the box across providers. Per-user registration can be offered as an additional option for advanced users or managed deployments.

---

## Things to Take Care About

**DNS providers must issue long-lived tokens or support token refresh — this is a hard requirement.**  

DDNS is the only Domain Connect use case that depends on persistent, unattended access to the DNS provider's API. A DNS provider that issues short-lived access tokens with no refresh token support cannot be used for DDNS at all: the client would lose write access after the first token expiry, silently breaking IP updates with no recourse short of the user re-running the entire setup flow.

DNS providers implementing the async flow for DDNS must therefore either:
- Issue access tokens with a lifetime long enough to be practical for unattended devices (months to years), or
- Issue refresh tokens alongside access tokens, allowing the client to obtain a new access token autonomously when the current one nears expiry.

Of the two, refresh token support is strongly preferred. Indefinitely long-lived access tokens are a security liability — if a token is leaked or a device is compromised, the attacker has permanent write access to the domain's A record. A refresh token flow allows token rotation and enables revocation (invalidating the refresh token ends access). DNS providers should support refresh tokens and clients should rotate them proactively.

**The DDNS client must implement OAuth token refresh.**  

Access tokens expire. The client must implement the refresh token cycle — requesting a new access token before the current one expires. If the client fails to refresh, it silently loses the ability to push updates. The domain stops resolving correctly, and the user has no visibility into this failure. Robust error handling and a re-authentication fallback (prompting the user to re-run the async flow) are essential.

**IP validation before every update.**  

The client must validate the IP before pushing an update. Common failure modes:
- `0.0.0.0` or `127.0.0.1` when the network interface is down or misconfigured
- A private RFC 1918 address (e.g. `192.168.x.x`) when the client detects the LAN interface instead of the WAN IP, or when NAT reflection causes the client to see its own private IP
- A stale IP from a cached response

An invalid IP pushed to a live DNS record breaks inbound connectivity for everyone trying to reach the domain. Validate: is the IP public? Is it reachable? Only push if confident.

**Token scope is limited — do not use for other operations.**  

The async token issued by the DNS provider is scoped to this specific template on this specific domain. It cannot be used to create other record types, manage other domains, or access the DNS provider's broader API. Do not attempt to use it for anything other than Domain Connect template updates.

**The reference client implementation.**  

The [DomainConnectDDNS](https://github.com/Domain-Connect/DomainConnectDDNS) open-source client is the reference implementation of the DDNS async flow. Study it before building your own client — it demonstrates correct token storage, refresh handling, and update call construction.

---

## Specificities and Remarks

- **DDNS at a subdomain, not the apex.** The example template uses `@` as the host (apex). For DDNS at a subdomain (e.g. `home.yourdomain.com`), set `hostRequired: true` and keep `host: "@"`. The user specifies the subdomain during the async flow setup, and the `@` in host resolves to that subdomain.
- **Combining DDNS with other templates.** A home server operator may also want MX records for self-hosted mail, or a CNAME for a specific service. These are separate templates with separate `serviceId` values, applied independently. They coexist on the same domain because they cover different record types. The DDNS client only ever updates the A/AAAA records covered by this template.
- **Update frequency and rate limiting.** DNS providers that implement Domain Connect may apply rate limits on template update calls. Design your client to update only when the IP actually changes (event-driven, not on a polling interval), and implement exponential backoff on update failures.
- **The `domainconnect.org` templates are the protocol's own reference.** They are not tied to a commercial product — they exist to demonstrate the DDNS pattern and to be used by generic clients. Any DDNS platform that wishes to be interoperable should follow the same structure.
