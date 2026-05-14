# UC-09: DNS Subdomain Delegation

**Index:** [15_Template_Use_Cases.md](../15_Template_Use_Cases.md)  
**DNS records used:** NS (subdomain)  
**Complexity:** Medium

---

## Use Case Description

A service provider takes authoritative control over a specific subdomain zone within the user's domain by having the user's DNS provider create NS records at a chosen subdomain. Once delegated, all DNS queries for that subdomain and its children are answered exclusively by the provider's nameservers — the user's DNS provider is no longer consulted for any names within that subtree.

This is a structural DNS operation, not a content operation. The template does not create any actual resource records (A, MX, TXT, etc.) — it creates the zone cut that makes the provider's nameservers authoritative for the subdomain. All content within the delegated zone is then managed by the provider.

Typical products in this category:
- Protocol overlay services that use DNS as a structured data store (NUM, ENUM, NAPTR hierarchies)
- Managed sub-zone hosting (enterprise DNS providers managing a department or product subdomain)
- IoT device management platforms that need a per-customer DNS namespace
- Services that require frequent, programmatic DNS changes beneath a subdomain without touching the parent zone

---

## Value Added for the End User

NS delegation is one of the least-understood DNS operations. Most domain owners have never created an NS record outside of their zone's apex (where it is set by the registrar, not the user). The correct syntax, the number of NS records required, and the concept of a zone cut are all non-obvious.

A manual delegation also has a zero-tolerance error profile: a single typo in an NS hostname means the entire delegated zone is unreachable. There is no partial failure — it either works or it does not.

With a Domain Connect template, the provider injects the correct NS hostnames as variables, the DNS provider creates all four records atomically, and the user only approves a consent screen. The provider can also verify delegation immediately by querying the parent zone.

Key benefits:
- Atomic creation of all NS records — no partial delegation possible
- Provider controls the NS values — correct nameserver hostnames guaranteed
- Zone cut is established in a single consent-and-approve step
- User does not need to understand what an NS record or zone cut is

---

## Example Template

```json
{
  "providerId": "subzonehost.example",
  "providerName": "Acme SubZone",
  "serviceId": "delegate-subzone",
  "serviceName": "Acme SubZone DNS Delegation",
  "version": 1,
  "syncPubKeyDomain": "domainconnect.subzonehost.example",
  "syncRedirectDomain": "portal.subzonehost.example",
  "shared": true,
  "sharedProviderName": true,
  "description": "Delegates DNS authority for a subdomain of your domain to Acme SubZone nameservers. All DNS records under this subdomain will be managed by Acme SubZone.",
  "records": [
    {
      "groupId": "ns-delegation",
      "type": "NS",
      "host": "%subzone%",
      "pointsTo": "%ns1%.subzonehost.example",
      "ttl": 3600
    },
    {
      "groupId": "ns-delegation",
      "type": "NS",
      "host": "%subzone%",
      "pointsTo": "%ns2%.subzonehost.example",
      "ttl": 3600
    },
    {
      "groupId": "ns-delegation",
      "type": "NS",
      "host": "%subzone%",
      "pointsTo": "%ns3%.subzonehost.example",
      "ttl": 3600
    },
    {
      "groupId": "ns-delegation",
      "type": "NS",
      "host": "%subzone%",
      "pointsTo": "%ns4%.subzonehost.example",
      "ttl": 3600
    }
  ]
}
```

---

## Explanation of Key Template Setup

### NS records at a variable subdomain

The `%subzone%` variable is the subdomain being delegated — for example `_num`, `services`, `iot`, or `api`. The provider's backend injects this value when constructing the Domain Connect URL. The four NS records all share the same `host` value and together form the complete NS RRset for the delegation.

Having all four records in a single `groupId` (`"ns-delegation"`) ensures the DNS provider creates them atomically. An NS RRset with only one or two records would function but reduces redundancy; partial application should not be possible.

### NS target hostnames as variables

The nameserver hostnames (`%ns1%` through `%ns4%`) are injected by the provider. They typically follow a pattern like `ns1.subzonehost.example`, `ns2.subzonehost.example`, etc. Using variables rather than hardcoded hostnames gives the provider flexibility to assign different nameserver clusters per customer or per region.

If your nameserver hostnames are identical for all customers, hardcoding them is simpler and removes any risk of injection error:

```json
{
  "groupId": "ns-delegation",
  "type": "NS",
  "host": "%subzone%",
  "pointsTo": "ns1.subzonehost.example",
  "ttl": 3600
}
```

### `shared: true` and `sharedProviderName: true`

NS delegation at a specific subdomain does not conflict with other Domain Connect services on the same domain (which typically operate at `@` or at different subdomains). Setting `shared: true` signals that this template is designed to coexist with other services on the domain.

### TTL of 3600

Unlike DDNS (where 60 seconds is correct), NS records for a stable subdomain delegation should use a standard TTL of 3600 or higher. The NS RRset for a delegated zone is cached by resolvers for the duration of the TTL — a short TTL generates high query load on the parent zone's DNS provider for no benefit.

---

## Template Examples in the Public Repository

- [numserver.com / delegate-num-zone](https://github.com/domain-connect/Templates/blob/master/numserver.com.delegate-num-zone.json) — four NS records at `_num` pointing to four nameserver hostnames across different TLDs (`.com`, `.org`, `.uk`, `.net`); uses variable NS targets and `shared: true`

---

## Things to Take Care About

**Not all DNS providers support NS records at arbitrary subdomains.**  
Creating NS records at subdomains (other than the apex) requires the DNS provider to correctly implement zone cut semantics. Some DNS hosting platforms restrict NS record creation to the apex zone, or require special configuration to enable it. Before building a product on this pattern, test explicitly against each DNS provider whose Domain Connect implementation you intend to support. Do not assume support based on general DNS capability.

**Zone cut makes parent-zone records at that subdomain invisible.**  
Once NS records are created at `services.yourdomain.com`, the DNS resolver stops consulting the parent zone for any name at or below `services.yourdomain.com`. Any records the user previously had at that subdomain in their DNS provider panel become unreachable — they exist in the parent zone but are shadowed by the zone cut. Make sure users understand this in your onboarding UI.

**Glue records cannot be created via Domain Connect.**  
Glue records (A records for nameserver hostnames that are within the delegated zone) must be created in the parent zone and are managed by the parent DNS provider, not the child zone operator. Domain Connect has no mechanism for glue record creation. To avoid this complication entirely, always use out-of-zone nameserver hostnames — i.e., NS targets that are not within the subdomain being delegated. The example template follows this rule: `ns1.subzonehost.example` is outside `yourdomain.com` and requires no glue.

**Revoking the delegation is the provider's responsibility.**  
When a customer cancels, the NS records must be removed from the parent zone. If they remain, queries for the delegated subdomain are sent to nameservers that may no longer be authoritative for it, resulting in SERVFAIL responses for all names in the zone. Implement a deprovisioning flow that either revokes the template via the Domain Connect async delete mechanism (if the DNS provider supports it) or instructs the user to remove the NS records manually.

**Four NS records is a minimum for production.**  
RFC 2182 recommends at least three nameservers per zone, located in different administrative and topological locations. Using four is common practice. Do not create a delegation with a single NS record — the zone becomes unreachable if that nameserver is unavailable.

---

## Specificities and Remarks

- **Protocol overlay services** are the primary driver of this pattern in the wild. The NUM protocol (and similar DNS-as-structured-data approaches) require a dedicated subdomain zone per domain owner. Domain Connect makes enrolling thousands of domain owners practical — without it, the friction of NS delegation would limit adoption to technically sophisticated users.
- **Enterprise sub-zone management.** Large organisations sometimes delegate a subdomain (e.g. `mail.company.com` or `api.company.com`) to a specialised DNS management service. Domain Connect can automate the parent-zone NS record creation, while the child zone operator manages the content.
- **The `%subzone%` variable should be validated server-side.** If the subdomain is user-supplied, validate it before injecting: it must be a valid DNS label (letters, digits, hyphens; no leading hyphen; max 63 characters), and it must not conflict with the provider's own infrastructure or reserved names.
- **NS delegation versus CNAME delegation for DMARC/DKIM.** In [UC-03](./UC-03_Email_Security_DMARC.md), CNAME delegation is used for `_dmarc` and optionally NS delegation for `_domainkey`. The choice between CNAME and NS for email security records is a product decision: CNAME delegation (per record) is more targeted; NS delegation (entire subtree) is more powerful but gives the provider complete control. Both patterns appear in the repository.
