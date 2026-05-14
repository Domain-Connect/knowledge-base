# UC-01: Email Hosting

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**DNS records used:** MX, SPFM, TXT (DKIM), CNAME (autodiscover/autoconfig)  
**Complexity:** Medium–High

---

## Use Case Description

A service provider hosts email mailboxes on behalf of the domain owner. The user's domain receives email through the provider's mail infrastructure. This is the most complete email template pattern: it configures inbound mail routing (MX), outbound authentication (SPF, DKIM), spoofing protection (DMARC), and optionally client auto-discovery so that desktop/mobile mail clients configure themselves automatically.

Typical products in this category:
- Business email suites (hosted @yourdomain.com mailboxes)
- Email-as-a-service platforms bundled with website builders
- White-label hosted email for agencies and resellers

---

## Value Added for the End User

Without Domain Connect, connecting a custom domain to a hosted email service means locating the provider's DNS instructions, navigating the registrar's control panel, creating 5–8 records one by one, waiting for propagation, and then troubleshooting when something is wrong. Drop-off rates exceed 50% on this task.

With a Domain Connect template, the user clicks "Connect my domain" in the provider's dashboard, is redirected to their DNS provider's consent screen, reviews what will change, and clicks Approve. All records are created in seconds. The complexity of MX priorities, DKIM key formatting, and SPF merge semantics is handled entirely by the protocol.

Key benefits:
- Eliminates the most error-prone DNS task (manual MX + SPF configuration)
- Users see a consent screen with plain-language record descriptions — not raw DNS syntax
- SPF is applied as a merge (SPFM record type), preserving any existing SPF policy on the domain
- Correct DKIM and DMARC records are set from day one, improving deliverability immediately

---

## Example Template

```json
{
  "providerId": "mailhost.example",
  "providerName": "Acme Mail",
  "serviceId": "hosted-email",
  "serviceName": "Acme Mail — Business Email Hosting",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.mailhost.example",
  "syncRedirectDomain": "app.mailhost.example",
  "description": "Configure DNS records for Acme Mail. Sets up MX, SPF, DKIM, DMARC, and mail client auto-discovery.",
  "records": [
    {
      "groupId": "mx",
      "type": "MX",
      "host": "@",
      "pointsTo": "mx1.mailhost.example",
      "priority": 10,
      "ttl": 3600
    },
    {
      "groupId": "mx",
      "type": "MX",
      "host": "@",
      "pointsTo": "mx2.mailhost.example",
      "priority": 20,
      "ttl": 3600
    },
    {
      "groupId": "spf",
      "type": "SPFM",
      "host": "@",
      "spfRules": "include:spf.mailhost.example"
    },
    {
      "groupId": "dkim",
      "type": "TXT",
      "host": "%dkimSelector%._domainkey",
      "data": "%dkimPublicKey%",
      "ttl": 3600
    },
    {
      "groupId": "dmarc",
      "type": "TXT",
      "host": "_dmarc",
      "data": "v=DMARC1; p=quarantine; rua=mailto:dmarc@dmarc.example; fo=1",
      "ttl": 3600,
      "txtConflictMatchingMode": "Prefix",
      "txtConflictMatchingPrefix": "v=DMARC1"
    },
    {
      "groupId": "autodiscover",
      "type": "CNAME",
      "host": "autodiscover",
      "pointsTo": "autodiscover.mailhost.example",
      "ttl": 3600
    },
    {
      "groupId": "autodiscover",
      "type": "CNAME",
      "host": "autoconfig",
      "pointsTo": "autoconfig.mailhost.example",
      "ttl": 3600
    }
  ]
}
```

---

## Explanation of Key Template Setup

### MX records — two entries, different priorities

Two MX records provide redundancy. Priority 10 is the primary relay; priority 20 is the fallback. Both use fixed `pointsTo` values (no variables) because the mail infrastructure is the same for all customers. If your infrastructure requires a per-customer MX hostname, use a variable: `"pointsTo": "%mxHost%"`.

### SPFM — merge, not replace

The `SPFM` record type is specific to Domain Connect. It does **not** create a new `TXT "v=spf1 ..."` record. Instead, the DNS provider merges the `spfRules` value into the existing SPF policy on the domain. This is critical: many domains already have an SPF record (e.g. from Google Workspace or another sender). A plain TXT replacement would break existing SPF. Always use `SPFM` for SPF — never a raw `TXT` with `v=spf1`.

### DKIM — variable selector and public key

DKIM requires a per-customer or per-rotation key. The `%dkimSelector%` variable becomes the subdomain prefix (e.g. `s1._domainkey`), and `%dkimPublicKey%` is the full DKIM TXT record value your service generates. Your service must pass these values when invoking the template via the API.

### DMARC — conflict-aware TXT placement

The `txtConflictMatchingMode: "Prefix"` with `txtConflictMatchingPrefix: "v=DMARC1"` tells the DNS provider to replace any existing DMARC record rather than add a duplicate. Without this, re-applying the template would accumulate multiple `_dmarc` TXT records, making DMARC evaluation unpredictable.

### Autodiscover / Autoconfig CNAMEs

`autodiscover` is used by Microsoft Outlook and Exchange clients; `autoconfig` is used by Mozilla Thunderbird and many mobile clients. Adding both ensures that any desktop or mobile mail client can self-configure by querying these hostnames. These are optional but strongly recommended for a complete hosted-email template.

### groupId — structured consent and selective application

Each logical function (MX routing, SPF, DKIM, DMARC, autodiscovery) is assigned its own `groupId`. This allows DNS providers to display grouped consent (the user sees "mail routing", "authentication", "auto-discovery" as separate items) and allows future template updates to affect only specific groups without disturbing others.

---

## Template Examples in the Public Repository

- [atlos.email / mail](https://github.com/domain-connect/Templates/blob/master/atlos.email.mail.json) — full stack: MX, SPF, DKIM (ed25519), DMARC, autodiscover/autoconfig CNAMEs
- [titan.email / titan-mail-hosting](https://github.com/domain-connect/Templates/blob/master/titan.email.titan-mail-hosting.json) — lean template: MX + SPF only, grouped
- [microsoft.com / O365](https://github.com/domain-connect/Templates/blob/master/microsoft.com.o365.json) — complex multi-service template with MX, SPF, DKIM (CNAME-based), SRV (Skype), MDM CNAMEs, and a TXT verification record

---

## Things to Take Care About

**SPF: always SPFM, never raw TXT.**  
Using a `TXT` record with `v=spf1 ...` instead of `SPFM` will overwrite the user's existing SPF policy. The DNS provider's conflict resolution will either reject the record or replace the existing one. Both outcomes break other senders that rely on the current SPF.

**DKIM key rotation.**  
Your template creates a DKIM record that is static once applied. Plan for key rotation: either use a fixed selector that your service rotates on its own infrastructure (CNAME-based DKIM, as Microsoft 365 does), or design a process to re-apply the template with a new selector when rotating. Document this for your users.

**DMARC policy strength.**  
Starting with `p=quarantine` is a reasonable default for a new email hosting template. Do not default to `p=reject` without user understanding — it can immediately block legitimate mail from other senders not yet covered by DKIM or SPF. Consider making the policy a variable so users can progress from `none` → `quarantine` → `reject`.

**Don't conflict with existing MX records.**  
If a user already has MX records pointing elsewhere (e.g. a different email provider), your new MX records will conflict. Domain Connect DNS providers are expected to handle this via conflict resolution, but some providers replace rather than merge MX. Inform users in your UI that applying the template will replace existing MX records — this is a hard cutover, not an additive change.

**`warnPhishing` flag.**  
Consider setting `"warnPhishing": true` if your template creates records that could be misused for phishing (e.g. MX records enabling impersonation of any domain). DNS providers that support this flag will show an additional warning in the consent screen.

---

## Specificities and Remarks

- **CNAME-based DKIM** (as used by Microsoft 365 and several ESPs) is an alternative pattern to placing the DKIM TXT record directly. The CNAME points to a provider-controlled hostname where the actual key lives, enabling the provider to rotate keys without requiring the user to update DNS. This requires DNS providers to support CNAME resolution at `_domainkey` subdomains — most do, but it is worth testing.
- **SRV records** for mail protocol auto-discovery (IMAP, SMTP) follow [RFC 6186](https://datatracker.ietf.org/doc/html/rfc6186). They are supported in Domain Connect but rarely included in templates, as autodiscover/autoconfig CNAME-based discovery is more widely implemented by mail clients.
- **Multiple MX priorities** in a template are additive — the DNS provider creates all of them. If the user has pre-existing MX records, conflict resolution varies by provider; most replace rather than merge MX sets.
- **`syncBlock: false`** (the default) means your template supports both synchronous (OAuth-based) and asynchronous flows. For hosted email, the synchronous flow is preferred because the user experience is smoother — the DNS change and the account activation happen in one browser session.
