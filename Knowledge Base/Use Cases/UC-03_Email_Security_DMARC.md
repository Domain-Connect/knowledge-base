# UC-03: Email Security & DMARC Management

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**DNS records used:** CNAME (_dmarc), SPFM, NS (_domainkey), CNAME (MTA-STS, TLSRPT), NS (_bimi)  
**Complexity:** Medium–High

---

## Use Case Description

A service provider specialises in monitoring and enforcing email security standards on behalf of the domain owner. The provider takes control of the DMARC record (and optionally SPF, DKIM, MTA-STS, TLSRPT, and BIMI) in order to provide centralised visibility, policy management, and incident alerting.

The distinguishing feature of this use case is that the DNS records **delegate control to the provider's infrastructure** rather than setting static values. The canonical pattern is a CNAME at `_dmarc` pointing to the provider's reporting pipeline. This allows the provider to update the DMARC policy, reporting addresses, and forensic options without any further DNS changes.

Typical products in this category:

- DMARC monitoring and enforcement platforms
- Email security posture management tools
- Managed email security services offered by MSSPs
- Compliance-driven email authentication products

---

## Value Added for the End User

DMARC adoption stalls at the "getting the first record in" step. The correct syntax, the right reporting URIs, and the distinction between `p=none`, `p=quarantine`, and `p=reject` are all non-obvious. Most organisations spend weeks in the monitoring phase without progressing to enforcement, because interpreting DMARC aggregate reports requires expertise.

A DMARC management platform solves this by becoming the authoritative source of the DMARC policy for the domain. The user connects their domain once (via Domain Connect), and the provider manages everything thereafter: policy progression, report ingestion, DKIM key inventory, and alerts. The Domain Connect template is the mechanism for establishing this delegation in a single, consent-driven step.

Key benefits:

- Zero-friction DMARC onboarding: one click instead of a multi-step DNS walkthrough
- Policy is managed server-side — no further DNS changes required for policy progression
- Reduces time from signup to `p=reject` enforcement from weeks to days
- DKIM and SPF visibility comes automatically once reporting starts

---

## Example Template

```json
{
  "providerId": "emailguard.example",
  "providerName": "Acme EmailGuard",
  "serviceId": "managed-email-security",
  "serviceName": "Acme EmailGuard — Managed DMARC",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.emailguard.example",
  "syncRedirectDomain": "portal.emailguard.example",
  "warnPhishing": true,
  "description": "Delegates DMARC policy management to Acme EmailGuard. Also configures SPF, MTA-STS, and TLSRPT.",
  "records": [
    {
      "groupId": "dmarc",
      "type": "CNAME",
      "host": "_dmarc",
      "pointsTo": "%dmarcCname%.emailguard.example",
      "ttl": 3600
    },
    {
      "groupId": "spf",
      "type": "SPFM",
      "host": "@",
      "spfRules": "%spfRules%"
    },
    {
      "groupId": "dkim-ns",
      "type": "NS",
      "host": "_domainkey",
      "pointsTo": "%ns1%.emailguard.example",
      "ttl": 3600
    },
    {
      "groupId": "dkim-ns",
      "type": "NS",
      "host": "_domainkey",
      "pointsTo": "%ns2%.emailguard.example",
      "ttl": 3600
    },
    {
      "groupId": "mta-sts-policy",
      "type": "CNAME",
      "host": "mta-sts",
      "pointsTo": "%mtaStsPolicy%.emailguard.example",
      "ttl": 3600
    },
    {
      "groupId": "mta-sts-txt",
      "type": "CNAME",
      "host": "_mta-sts",
      "pointsTo": "%mtaStsTxt%.emailguard.example",
      "ttl": 600
    },
    {
      "groupId": "tlsrpt",
      "type": "CNAME",
      "host": "_smtp._tls",
      "pointsTo": "%tlsrpt%.emailguard.example",
      "ttl": 3600
    }
  ]
}
```

---

## Explanation of Key Template Setup

### DMARC CNAME delegation — the core pattern

Instead of placing a static `TXT "v=DMARC1; p=none; ..."` record, this template places a **CNAME** at `_dmarc` pointing to the provider's infrastructure. When a receiving mail server queries `_dmarc.yourdomain.com`, the CNAME leads to the provider's TXT record, which the provider controls entirely. This enables:

- Policy changes (`none` → `quarantine` → `reject`) without user DNS changes
- Reporting address management without user DNS changes
- Multi-domain policy inheritance (the CNAME can resolve to a shared policy record)

This pattern requires the receiving mail server to follow the CNAME — which [RFC 7489](https://datatracker.ietf.org/doc/html/rfc7489) (DMARC) and [RFC 9091](https://datatracker.ietf.org/doc/html/rfc9091) (DMARC organisational domain) permit. All major mail receivers (Google, Microsoft, Yahoo) follow CNAMEs at `_dmarc`.

### NS delegation for `_domainkey`

Delegating `_domainkey` via NS records hands the entire DKIM namespace for the domain to the provider. The provider can then create, rotate, and retire DKIM selectors without the user ever touching DNS again. This is the most comprehensive DKIM management option — appropriate for fully managed email security, where the provider controls all signing infrastructure.

This is a powerful but consequential change: no other party can add DKIM records for this domain without going through the provider. Make this clear in the consent screen description for the `dkim-ns` group.

### MTA-STS and TLSRPT

MTA-STS ([RFC 8461](https://datatracker.ietf.org/doc/html/rfc8461)) enforces TLS for inbound SMTP delivery. It requires two records:

- `mta-sts.yourdomain.com` (CNAME or A) — serves the policy document
- `_mta-sts.yourdomain.com` (TXT) — signals that MTA-STS is active

TLSRPT ([RFC 8460](https://datatracker.ietf.org/doc/html/rfc8460)) at `_smtp._tls.yourdomain.com` enables receiving TLS failure reports.

Using CNAMEs for both lets the provider manage the policy text and update it without further DNS changes. The `_mta-sts` CNAME has a short TTL (600s) because mail senders cache the policy for 24h–30d and a short TTL helps propagate policy changes faster.

### `warnPhishing: true`

This template delegates significant control — DMARC policy, DKIM signing authority — to a third party. Setting `warnPhishing: true` prompts DNS providers that support this flag to display an additional warning in the consent screen. This is appropriate for any template that materially changes who can control email authentication for the domain.

### Minimal variant

A minimal DMARC management template is just:

```json
{
  "groupId": "dmarc",
  "type": "CNAME",
  "host": "_dmarc",
  "pointsTo": "%dmarcCname%.emailguard.example",
  "ttl": 3600
}
```

Start here and add groups progressively as your platform's capabilities expand.

---

## Template Examples in the Public Repository

- [palisade.email / managed-dmarc](https://github.com/domain-connect/Templates/blob/master/palisade.email.managed-dmarc.json) — minimal CNAME delegation: single `_dmarc` CNAME with a per-domain variable target
- [sendmarc.com / protection](https://github.com/domain-connect/Templates/blob/master/sendmarc.com.protection.json) — comprehensive: DMARC CNAME + SPFM + MTA-STS pair + TLSRPT + NS delegation for `_domainkey` and `_bimi`

---

## Things to Take Care About

**CNAME at `_dmarc` is not universally accepted by DNS providers.**  

Some DNS providers (particularly those with strict record-type validation) refuse to create a CNAME at `_dmarc` because [RFC 1912](https://datatracker.ietf.org/doc/html/rfc1912) discourages CNAMEs at names that also have other record types. In practice, `_dmarc` is a dedicated subdomain with no other records, so this is safe — but you may encounter implementation quirks. Test against your target DNS providers before deploying.

**The CNAME must resolve to a valid DMARC TXT record.**  

When a mail receiver queries `_dmarc.yourdomain.com` and gets a CNAME to `abc123.emailguard.example`, it will then query `abc123.emailguard.example` for a TXT record containing `v=DMARC1; ...`. If that record is missing or misconfigured, the domain has no effective DMARC policy. Your platform infrastructure must be ready before the user applies the template.

**NS delegation for `_domainkey` requires authoritative DNS support.**  

Not all DNS providers allow NS records at arbitrary subdomains. The `_domainkey` NS delegation pattern is powerful but may not work in all DNS hosting environments. Always check if the target DNS provider supports subdomain NS delegation in Domain Connect before relying on this as your primary DKIM management mechanism.

**Revoking the template.**  

When a customer cancels their subscription, you must revoke the template (via the Domain Connect async delete flow, if implemented) or instruct the user to remove the DNS records. A dangling `_dmarc` CNAME pointing to a deprovisioned provider record means the domain effectively has no DMARC policy — which can be exploited for spoofing. Implement lifecycle management for your DNS delegations.

**BIMI delegation (NS at `_bimi`)** follows the same pattern as `_domainkey` NS delegation. BIMI (Brand Indicators for Message Identification) requires a Verified Mark Certificate from an approved authority. Only use this if your platform actively manages BIMI, as a misconfigured BIMI record can suppress brand logo display in supported mail clients.

---

## Specificities and Remarks

- **`hostRequired: true`** is used by some DMARC providers to require the user to specify a subdomain prefix when applying the template. This supports multi-domain or sub-organisation use cases where the same provider instance manages multiple related domains. Most DMARC templates do not need this — apply it only if your onboarding flow is genuinely host-scoped.
- **SPF in a DMARC template** is optional but valuable. If your platform also optimises or enforces SPF, include an SPFM group. If it does not, omit SPF — a DMARC management platform that silently modifies SPF without the user understanding the scope would generate confusion and support load.
- **Aggregate vs forensic reports.** The `rua` tag in your DMARC record specifies aggregate report destinations; `ruf` specifies forensic (failure) report destinations. When using CNAME delegation, both are controlled by your platform. Inform users in your UI what data you collect and retain, particularly for forensic reports which may contain full email headers.
- **DMARC policy progression.** Best practice is to start customers at `p=none` (monitoring only), progress to `p=quarantine` after 30 days of clean reporting, and finally to `p=reject` once all legitimate sending sources are authenticated. The CNAME delegation model is ideal for automating this progression without user involvement.
