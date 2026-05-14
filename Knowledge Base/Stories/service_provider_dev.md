# Service Provider Developer — "One JSON file replaced sixteen help pages"

*Part of the [Domain Connect Storytelling](../14_Storytelling.md) collection*

---

Before Domain Connect, my relationship with DNS configuration was a maintenance burden I hadn't fully accounted for when we first built our onboarding flow.

We had a DNS setup guide. It was a static page with screenshots for each major registrar. GoDaddy looked like this, IONOS looked like that, Cloudflare had a slightly different field layout. We'd built it once and then kept patching it. Registrar changes their UI, screenshots go stale, customers fail, someone files a bug, I update the screenshots.

The deeper problem was that the guide was also the source of truth for customer success. If a customer configured their DNS wrong, the only way to detect it was to poll their records ourselves and check. We'd built a record verifier that ran after setup. When it found a wrong value, we'd surface an error message telling the customer what it should be. They'd go back to their registrar, try to find the right field, and often make it worse. The verification loop was unpleasant for the customer and expensive for us.

When the product team asked me to evaluate Domain Connect, I started with the template format. It's a JSON file. You declare what records you need:

```json
{
  "providerId": "ourservice.com",
  "serviceId": "email",
  "records": [
    { "type": "MX", "host": "@", "pointsTo": "mail.ourservice.com.", "priority": 10, "ttl": 3600 },
    { "type": "TXT", "host": "@", "data": "ourservice-verify=%VERIFYTOKEN%", "ttl": 3600,
      "txtConflictMatchingMode": "Prefix", "txtConflictMatchingPrefix": "ourservice-verify=" }
  ]
}
```

That's the core of it. Variable `%VERIFYTOKEN%` is per-customer — we pass it in the redirect URL. The DNS provider substitutes it. We never built per-registrar logic. We never wrote registrar-specific documentation. We described what we need once, and every DNS provider that has deployed our template knows how to apply it.

The service provider implementation has three moving parts. First, the template itself — I based ours on a similar service's template in the public repository, which made the first draft much faster and gave me a clear starting point for the review process. Second, URL signing — the spec gives you the exact canonical form of the parameters, the signing algorithm (RS256), and how to publish the public key in DNS. I had a working implementation in about a day. Third, the discovery flow in our onboarding UI — three API calls to check whether the customer's DNS provider supports Domain Connect and has our template deployed, and if yes, show the "Connect automatically" button instead of the manual instructions.

The end-to-end integration took our team about three weeks. The template review process added some time — the Domain Connect community reviews PRs, and there were a few back-and-forth rounds about variable scope and SPF record handling. Once the template was merged, we started contacting DNS providers to deploy it.

The maintenance profile is completely different now. The template doesn't need to change when a registrar updates their UI — that's the registrar's problem, not ours. Our verification logic is simpler because Domain Connect applications are deterministic: if it succeeded, the records are correct. The edge cases we still handle are customers whose DNS providers don't yet support Domain Connect, which is a shrinking set.

The thing I'd tell any developer implementing the service provider side: start from an existing template in the repository, use the online editor to validate and test variable substitution before submitting, and test your URL signing against the example service's signature tool before going anywhere near production. Those three steps catch the vast majority of implementation issues before they hit review.

---

*Back to: [Storytelling Index](../14_Storytelling.md)*
