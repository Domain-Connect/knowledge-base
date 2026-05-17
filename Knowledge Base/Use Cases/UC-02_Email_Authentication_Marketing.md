# UC-02: Email Authentication & Marketing

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**DNS records used:** SPFM, TXT (DKIM), CNAME (return path, tracking, DKIM delegation)  
**Complexity:** Low–Medium

---

## Use Case Description

A service provider sends email **on behalf of** the domain owner — newsletters, transactional notifications, marketing campaigns — but does not host the mailboxes. The domain owner retains their existing email setup (e.g. Google Workspace, Microsoft 365). The template adds the authentication layer that tells receiving mail servers that the service provider is an authorised sender for this domain.

This is the most common email-related template pattern in the repository. It covers:

- Email marketing platforms (newsletters, campaigns)
- Transactional email APIs (order confirmations, password resets)
- CRM and sales automation tools that send outbound email
- Any SaaS tool with an "authenticated sending domain" or "custom sender domain" feature

The minimal set is **SPF + DKIM**. More complete templates also add a return-path CNAME (for bounce handling) and a click/open-tracking CNAME.

---

## Value Added for the End User

Email deliverability depends on SPF and DKIM being correctly configured. Without them, marketing email lands in spam or is rejected outright. The configuration itself is non-trivial: DKIM requires generating a keypair, placing the public key as a TXT record at a specific subdomain, and then verifying it — a process that typically involves copying a long cryptographic string and is highly error-prone.

With a Domain Connect template, the service provider generates the DKIM key, encodes it as a template variable, and invokes the DNS change on behalf of the user. The user sees a consent screen, approves, and the domain is authenticated. What previously required a 10-step help article now happens in a single OAuth flow.

Key benefits:

- Domain authentication is completed correctly on the first attempt
- SPF merge semantics (SPFM) prevent breaking existing SPF policy
- Dramatically reduces support tickets related to failed domain verification
- Users reach the "sending" state faster, reducing time-to-value for the service

---

## Example Template

```json
{
  "providerId": "mailerplatform.example",
  "providerName": "Acme Mailer",
  "serviceId": "domain-auth",
  "serviceName": "Acme Mailer Domain Authentication",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.mailerplatform.example",
  "syncRedirectDomain": "app.mailerplatform.example",
  "description": "Authenticates your domain for sending via Acme Mailer. Sets up SPF, DKIM, return-path, and click tracking.",
  "records": [
    {
      "groupId": "spf",
      "type": "SPFM",
      "host": "@",
      "spfRules": "include:spf.mailerplatform.example"
    },
    {
      "groupId": "dkim",
      "type": "TXT",
      "host": "%dkimSelector%._domainkey",
      "data": "%dkimPublicKey%",
      "ttl": 3600
    },
    {
      "groupId": "returnpath",
      "type": "CNAME",
      "host": "bounces",
      "pointsTo": "returnpath.mailerplatform.example",
      "ttl": 3600
    },
    {
      "groupId": "tracking",
      "type": "CNAME",
      "host": "click",
      "pointsTo": "tracking.mailerplatform.example",
      "ttl": 3600
    }
  ]
}
```

---

## Explanation of Key Template Setup

### SPFM — merging SPF, not replacing it

The `SPFM` type merges the `spfRules` value into the domain's existing `v=spf1` record. The DNS provider handles the merge logic. This is essential for marketing platform templates: the user almost certainly has an existing SPF record for their primary email provider. A raw `TXT` SPF record would either conflict or overwrite it, breaking other senders. Always use `SPFM`.

### DKIM — variable selector and key

`%dkimSelector%` is the subdomain prefix (e.g. `s1`, `mailer1`, `em7859`). `%dkimPublicKey%` is the full DKIM TXT record value, typically in the format `v=DKIM1; k=rsa; p=<base64-encoded-key>`. Both values are injected by the service's backend when it initiates the Domain Connect flow for a specific user domain.

Some providers prefer CNAME-based DKIM delegation instead of placing the raw key directly. In that pattern, the TXT record is replaced by a CNAME pointing to the provider's infrastructure:

```json
{
  "groupId": "dkim",
  "type": "CNAME",
  "host": "%dkimSelector%._domainkey",
  "pointsTo": "%dkimCnameTarget%",
  "ttl": 3600
}
```

CNAME delegation allows the provider to rotate keys without requiring the user to update DNS. This is the preferred approach for large-scale ESPs with frequent key rotation schedules. See the SendGrid pattern in the examples below.

### Return-path CNAME

The return-path (or bounce domain) CNAME routes bounced emails back to the provider's infrastructure under the user's own domain. This improves deliverability by keeping the bounce-handling domain aligned with the sending domain. The subdomain (`bounces` in this example) must match what your platform uses when constructing the `Return-Path` header.

### Tracking CNAME

Click and open tracking requires links and pixel URLs to be served from the user's own domain (e.g. `click.yourdomain.com`). This CNAME proxies those requests to the provider's tracking infrastructure. It is optional but improves deliverability with strict inbox providers and enables first-party tracking (important as third-party cookie restrictions tighten).

### No MX records

Unlike UC-01 (Email Hosting), this pattern does **not** set MX records. The domain's existing mailboxes are unaffected. Adding MX records here would intercept the user's incoming mail — a destructive change that should never be done silently. If your platform also needs to receive bounces via SMTP (rather than through a CNAME return-path), use a distinct MX host on a subdomain, not on `@`.

---

## Template Examples in the Public Repository

- [sendgrid.com / domain-auth](https://github.com/domain-connect/Templates/blob/master/sendgrid.com.domain-auth.json) — CNAME-based DKIM delegation (3 CNAMEs: subdomain + 2 DKIM selectors), no SPF or MX
- [mailersend.com / mailersend-email](https://github.com/domain-connect/Templates/blob/master/mailersend.com.mailersend-email.json) — SPFM + TXT DKIM + return-path CNAME + tracking CNAME + inbound MX on a subdomain
- [brevo.com / domain-authentication](https://github.com/domain-connect/Templates/blob/master/brevo.com.domain-authentication.json) — comprehensive multi-group template with SPFM, TXT/CNAME DKIM options, DMARC, branded sending subdomain, return-path, image tracking, and optional NS delegation

---

## Things to Take Care About

**SPF lookup limit.**  

SPF has a hard limit of 10 DNS lookups per evaluation. If the user's existing SPF already has several `include:` directives, adding yours may push them over the limit, causing all SPF checks to fail (`permerror`). Alert users in your UI if their SPF record is close to the limit, and consider flattening your SPF include to a small CIDR list to reduce lookups.

**DKIM key length.**  

Use 2048-bit RSA keys minimum. 1024-bit keys are increasingly rejected by major inbox providers (Gmail, Microsoft 365). For new deployments, prefer ed25519 — it is shorter, faster to verify, and not subject to the RSA key-length arms race. Note that ed25519 DKIM is not yet supported by all receiving mail servers, so some providers deploy both RSA and ed25519 selectors.

**Selector naming collisions.**  

If `%dkimSelector%` is a static value (e.g. always `mailer1._domainkey`), and the user already has a DKIM record with that selector from a previous provider, your template will conflict. Either use a unique, per-deployment selector generated by your service, or use `txtConflictMatchingMode` to control replacement behaviour.

**Tracking subdomain conflicts.**  

The tracking CNAME subdomain (`click`, `open`, `track`, etc.) is often the same across all your customers. If the user has an existing record at that subdomain, the DNS provider's conflict handling will determine whether it is replaced. Document which subdomains your template claims so users can plan accordingly.

**CNAME-based DKIM requires DNS provider support.**  

Not all DNS providers correctly handle a CNAME at `selector._domainkey`. Some strip or reject CNAMEs at `_domainkey` subdomains. Before choosing CNAME delegation over raw TXT, confirm the DNS providers you care about support it. The public Domain Connect DNS provider implementations generally do, but self-hosted or less common providers may not.

---

## Specificities and Remarks

- **Multiple DKIM selectors** can be deployed simultaneously. Some providers include two DKIM groups in one template (e.g. `selector1` and `selector2`) to support seamless key rotation: the old selector stays active while the new one warms up. This is the pattern used by Microsoft 365.
- **`multiInstance: true`** is relevant if your platform is invoked multiple times for different sending domains on the same root domain (e.g. `newsletter.example.com` and `transactional.example.com`). Setting this flag allows the template to be applied more than once without the DNS provider treating it as a conflict.
- **Inbound MX on a subdomain** (e.g. `MX` on `bounces.@` or `inbound.@`) is a clean way to receive bounce notifications without touching the root MX. See the MailerSend template for an example of this pattern.
- **DMARC is not included** in this template because this use case does not own the domain's email identity — it shares it. Adding a DMARC record here would conflict with a policy already set by the primary email provider. If your platform also provides DMARC management, use a separate template (see [UC-03](./UC-03_Email_Security_DMARC.md)) or use `txtConflictMatchingMode` carefully.
