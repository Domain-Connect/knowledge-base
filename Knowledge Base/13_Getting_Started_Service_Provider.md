# 13 — Getting Started: Service Provider

*Part of the [Domain Connect Knowledge Base](./00_MASTER.md)*

*Sources: [domainconnect.org/getting-started](https://www.domainconnect.org/getting-started/), [11 — Template Reference](./11_Template_Reference.md), [draft-ietf-dconn-domainconnect-01](https://datatracker.ietf.org/doc/draft-ietf-dconn-domainconnect/)*

---

## Who this document is for

You offer a service — a website builder, email platform, SaaS product, or anything else — and you allow users to connect their own domain names to it. Right now, you send users to a help page with instructions to manually create DNS records. Half of them fail. This guide explains how to implement Domain Connect so the process becomes one click.

For the business case, see [06 — Value by Audience](./06_Value_by_Audience.md). For the full protocol overview, see [03 — How It Works](./03_How_It_Works.md).

---

## Start with the synchronous flow

If you are new to Domain Connect, start with the **synchronous flow**. It is:
- Simpler to implement than the asynchronous (OAuth) flow
- Supported by all ~20 DNS providers in the ecosystem
- Sufficient for the vast majority of service integrations — one-time setup where the user is present

The asynchronous flow is covered at the end of this document for services that need ongoing DNS management or multi-step flows.

---

## Step 1 — Define your template

Your template is a JSON file that describes exactly which DNS records your service requires. It is the foundation of everything else.

### Start from an existing template

Browse the template repository at **[github.com/Domain-Connect/Templates](https://github.com/Domain-Connect/Templates)** and find a template for a service similar to yours. Copy it and modify it. This is faster and more reliable than writing from scratch, and gives you a realistic starting point for the review process.

### Template essentials

At minimum your template needs:

```json
{
  "providerId": "yourcompany.com",
  "providerName": "Your Company",
  "serviceId": "website",
  "serviceName": "Your Service Name",
  "version": 1,
  "logoUrl": "https://yourcompany.com/logo.svg",
  "syncPubKeyDomain": "domainconnect.yourcompany.com",
  "syncRedirectDomain": "yourcompany.com",
  "records": [
    ...
  ]
}
```

`providerId` should be your company's domain name. `serviceId` identifies this specific service within your namespace. Together they form the primary key used in all API URLs and OAuth scopes.

### Design your records

List every DNS record your service needs to function. Keep records as **static as possible** — the less variable content, the more secure and easier to review. See [11 — Template Reference](./11_Template_Reference.md) for full field documentation.

**Common patterns:**

| Need | Record type | Example |
|------|-------------|---------|
| Point domain to your servers | A | `@ A 198.51.100.1` |
| Point `www` to your platform | CNAME | `www CNAME platform.yourcompany.com.` |
| Email routing | MX | `@ MX 10 mail.yourcompany.com.` |
| Domain ownership verification | TXT | `@ TXT "yourservice-verify=%TOKEN%"` |
| Email authentication | SPFM | `@ SPFM include:spf.yourcompany.com` |
| DKIM public key | TXT | `selector._domainkey TXT "v=DKIM1; k=rsa; p=%DKIMKEY%"` |

**Never use a plain SPF TXT record** (`v=spf1 ...`). Use `SPFM` instead — Domain Connect merges SPF entries from multiple templates automatically, and a raw SPF TXT record will conflict with other services' SPF records.

### Scope variables narrowly

Variables (`%VARNAME%`) should cover only the part of the record value that genuinely varies per user, not the entire value. Instead of:

```json
"pointsTo": "%FULLHOSTNAME%"
```

Prefer:

```json
"pointsTo": "%ACCOUNTID%.platform.yourcompany.com"
```

A narrower variable is harder to misuse, easier to review, and less likely to conflict with other templates. If your variable must be the full record value (e.g. an IP address), that is acceptable — but be prepared to justify it during template review.

### Security flags

**`syncPubKeyDomain` (strongly recommended for all templates):** Enables cryptographic signing of apply URLs. Without it, an attacker who intercepts the redirect URL can change parameter values (e.g. substituting their own IP address) before the user sees the consent screen.

**`warnPhishing`:** A weaker fallback for when signing is not feasible. Causes DNS providers to display an extra warning. Do not use this together with `syncPubKeyDomain` — they are mutually exclusive.

**`syncBlock: true`:** Restricts the template to the asynchronous flow only. Use this if your template cannot support signing and you want to prevent synchronous flow usage.

See [08 — Security Model](./08_Security_Model.md) for full discussion.

### Validate your template

Use the **[Online Editor](https://domainconnect.paulonet.eu/dc/free/templateedit)** to:
- Check your template against the JSON schema
- Test variable substitution with custom input values
- Test group filtering
- Test against both zone apex and subdomain (`host` parameter) scenarios

Click **"Copy Markdown"** after testing — you will need this link when submitting a pull request.

The linter at **[github.com/Domain-Connect/dc-template-linter](https://github.com/Domain-Connect/dc-template-linter)** catches common mistakes before review.

---

## Step 2 — Implement URL signing

If your template uses `syncPubKeyDomain` (which it should), you need to:

1. **Generate an RSA key pair** (RS256 / RSASSA-PKCS1-v1_5 with SHA-256 is the mandatory supported algorithm)
2. **Publish the public key** in DNS as TXT records at `{key-label}.{syncPubKeyDomain}`:
   ```
   _dck1.domainconnect.yourcompany.com. IN TXT "p=1,a=RS256,d=<base64-encoded-public-key>"
   ```
   If the key is too long for one TXT record, split it across multiple records using sequential `p=` fragment indexes.
3. **Sign each apply URL** using the private key before redirecting the user

**Signing procedure:**
1. Take all apply request parameters except `sig` and `key`
2. URL-encode each parameter name and value
3. Sort parameters in ascending lexicographic order of the URL-encoded name
4. Concatenate as `name=value` pairs joined by `&`
5. Sign this canonical string using the private key (RS256)
6. Base64-encode the signature
7. Append `&sig=<encoded-sig>&key=<key-label>` to form the final URL

**Testing signatures:** A tool for testing and verifying signatures is available at **[exampleservice.domainconnect.org/sig](https://exampleservice.domainconnect.org/sig)**.

**Key rotation:** Publish new keys at a new label within `syncPubKeyDomain`. The `key` parameter in each apply request identifies which label to look up — so old and new keys can coexist during rollover.

---

## Step 3 — Publish your template

### Submit to the template repository

Fork **[github.com/Domain-Connect/Templates](https://github.com/Domain-Connect/Templates)** and open a Pull Request with:

- Your template file named `{providerId}.{serviceId}.json` in the repository root
- The PR template filled in completely (loads automatically when opening a PR on GitHub)
- The Online Editor test results link (from Step 1) in the designated field

The Domain Connect community reviews all PRs. Common reasons for revision requests:

| Issue | Fix |
|-------|-----|
| File naming wrong | Use `providerId.serviceId.json` exactly |
| Variable too broad (bare `@ TXT "%verification%"`) | Add a service-specific prefix: `@ TXT "yourservice-verify=%verification%"` |
| Variable in `host` for subdomain targeting | Use the `host` apply parameter instead |
| `%host%` written in the `host` field | Remove it — the protocol adds it automatically (causes doubling) |
| SPF as a TXT record | Use `SPFM` |
| Missing `syncPubKeyDomain` | Add it, or use `syncBlock`/`warnPhishing` with justification |
| Both `syncPubKeyDomain` and `warnPhishing` set | Remove `warnPhishing` |
| Missing `syncRedirectDomain` | Add it if you use `redirect_uri` |
| Missing `hostRequired` on a template with apex-incompatible records | Set `"hostRequired": true` |

Publishing to the repository is not the same as deploying to DNS Providers — it is a central reference, not an automatic deployment. DNS Providers pull from the repository and deploy templates individually through their own vetting process.

---

## Step 4 — Onboard with DNS Providers

Each DNS Provider deploys templates individually after their own review. Contact the DNS Providers most relevant to your users. Contact information is on the DNS Provider page at **[domainconnect.org](https://www.domainconnect.org)**.

Some DNS Providers will deploy your template after a quick review. Others require contractual terms or a more formal vetting process. Plan for this to take days to weeks per provider.

**Which providers to prioritize:** Start with the providers your users most commonly use. GoDaddy, IONOS, Cloudflare, Squarespace Domains, and WordPress.com collectively cover the majority of the customer base for most service providers. Between them they cover roughly 35% of the .com zone.

---

## Step 5 — Implement the discovery and redirect flow in your product

This is the client-side integration in your own application.

### Discovery flow

When a user enters their domain name in your interface:

1. **Look up `_domainconnect.<domain>`** as a DNS TXT record
   - If the record does not exist: Domain Connect is not supported for this domain → show manual instructions
2. **Fetch the settings document** at `https://{record-value}/v2/{domain}/settings`
   - If this fails: fall back to manual instructions
3. **Query template support**: `GET {urlAPI}/v2/domainTemplates/providers/{your-providerId}/services/{your-serviceId}`
   - `200` → Domain Connect is available → show "Connect automatically" button
   - `404` → DNS Provider does not have your template → show manual instructions

If Domain Connect is not available at any step, always fall back gracefully to manual DNS instructions. Never block the user from completing setup just because Domain Connect is unsupported.

### Redirect construction

When the user clicks "Connect":

```
{urlSyncUX}/v2/domainTemplates/providers/{providerId}/services/{serviceId}/apply
  ?domain={user-domain}
  &host={subdomain-if-applicable}
  &{VAR1}={value1}
  &{VAR2}={value2}
  &redirect_uri={your-callback-url}
  &sig={signature}
  &key={key-label}
```

- Supply values for all variables defined in your template
- Include `redirect_uri` (and ensure it matches `syncRedirectDomain` in your template) to receive the user back after the DNS Provider completes the flow
- Include `sig` and `key` if your template requires signing

**Optional parameters:** `groupId` (to apply only a subset of records), `providerName` / `serviceName` (if `sharedProviderName`/`sharedServiceName` are set in your template).

### Post-connection verification

After the DNS Provider redirects the user back to your `redirect_uri`:

1. Poll DNS to verify the expected records are now present
2. Do not assume records are immediately resolvable — DNS propagation takes time
3. Only activate the service once propagation is confirmed

### Open-source libraries

Ready-to-use client libraries handle discovery, redirect URL construction, and signature generation:

| Language | Repository |
|----------|-----------|
| Python | [github.com/Domain-Connect/domainconnect_python](https://github.com/Domain-Connect/domainconnect_python) |
| PHP | [github.com/gaalferov/ext-domain-connect](https://github.com/gaalferov/ext-domain-connect) |

A complete working example of a Service Provider implementation (template1 unsigned, template2 signed) is live at **[exampleservice.domainconnect.org/simple](https://exampleservice.domainconnect.org/simple)** with full source at **[github.com/domain-connect/exampleservice](https://github.com/domain-connect/exampleservice)**.

---

## Asynchronous flow (when you need it)

The synchronous flow covers most use cases. Use the asynchronous (OAuth) flow when:

- Your setup requires multiple steps — for example, first verify domain ownership via TXT record, then configure MX and CNAME records after verification succeeds
- Your service needs to update DNS records over time without the user being present (e.g. dynamic DNS, infrastructure changes)
- You need to manage DNS programmatically on an ongoing basis

**Trade-offs:** The async flow is more complex to implement. Fewer DNS providers support it (though major ones do). Each DNS Provider requires bilateral OAuth setup — there is no automatic onboarding from the template repository. Start with the synchronous flow, add async only if you have a specific need that the sync flow cannot satisfy.

**How to start with async:** Contact DNS Providers directly to establish OAuth credentials. Contact the Domain Connect community for guidance and to onboard the example service as a test OAuth partner.

---

## Resources

| Resource | URL |
|----------|-----|
| Template repository | [github.com/Domain-Connect/Templates](https://github.com/Domain-Connect/Templates) |
| Online Editor (template testing) | [domainconnect.paulonet.eu/dc/free/templateedit](https://domainconnect.paulonet.eu/dc/free/templateedit) |
| Signature testing tool | [exampleservice.domainconnect.org/sig](https://exampleservice.domainconnect.org/sig) |
| Example service (live demo) | [exampleservice.domainconnect.org/simple](https://exampleservice.domainconnect.org/simple) |
| Example service source | [github.com/domain-connect/exampleservice](https://github.com/domain-connect/exampleservice) |
| Python client library | [github.com/Domain-Connect/domainconnect_python](https://github.com/Domain-Connect/domainconnect_python) |
| PHP client library | [github.com/gaalferov/ext-domain-connect](https://github.com/gaalferov/ext-domain-connect) |
| Template linter | [github.com/Domain-Connect/dc-template-linter](https://github.com/Domain-Connect/dc-template-linter) |
| Specification | [datatracker.ietf.org/doc/draft-ietf-dconn-domainconnect](https://datatracker.ietf.org/doc/draft-ietf-dconn-domainconnect/) |
| Template field reference | [11 — Template Reference](./11_Template_Reference.md) |
| DNS Provider list | [domainconnect.org](https://www.domainconnect.org) |
| Community / Slack | [domainconnect.org/getting-started](https://www.domainconnect.org/getting-started/) |

---

## Quick-start checklist

- [ ] Template JSON written and named `{providerId}.{serviceId}.json`
- [ ] Template tested in Online Editor — test results link saved
- [ ] Template linter run with no blocking errors
- [ ] RSA key pair generated; public key published in DNS at `{key}`.`{syncPubKeyDomain}`
- [ ] Signing logic implemented and tested at exampleservice.domainconnect.org/sig
- [ ] PR opened in template repository with Online Editor test results link
- [ ] At least one DNS Provider contacted for template onboarding
- [ ] Discovery flow implemented in your product
- [ ] Redirect URL construction and signing implemented
- [ ] Post-redirect DNS verification implemented
- [ ] Full flow tested end-to-end with at least one DNS Provider
- [ ] Fallback to manual instructions working when Domain Connect is unavailable

---

*Previous: [12 — Getting Started: DNS Provider](./12_Getting_Started_DNS_Provider.md) | Back to: [00 — Master Index](./00_MASTER.md)*
