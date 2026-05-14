# DNS Provider Developer — "I was skeptical of protocols. Then I read the spec."

*Part of the [Domain Connect Storytelling](../14_Storytelling.md) collection*

---

When my manager told me we were going to implement Domain Connect, my first reaction was the standard developer skepticism about new protocols. Is this well-specified? Is there a reference implementation? Who else has done this, and can I look at their implementation?

I spent a day reading the IETF draft. It's not a long document. The protocol is well-scoped: specific endpoints, specific data formats, specific flows. The settings endpoint returns a defined JSON structure. The template query endpoint returns 200 or 404. The synchronous UX flow has a defined sequence of ten steps. There's no ambiguity about what "compliant" means.

The implementation surface for the synchronous flow is genuinely bounded. You need:

1. A `_domainconnect` TXT record in hosted zones (DNS layer, no code)
2. A settings endpoint — JSON, three required fields
3. A template query endpoint — does this template exist, yes or no
4. A UX flow: validate → auth → ownership check → consent screen → apply → redirect

The complex part is the template application logic — variable resolution, conflict detection, SPFM merging for SPF records. But there's a Python reference library for that. I pulled it into a test environment, fed it a zone file and a template, and it returned the correct change set on the first run. We didn't implement that logic from scratch; we wrapped the library with our zone data access layer.

URL signature verification was the other piece that required care. The spec describes the signing procedure precisely: canonical form of parameters, RS256, base64 encoding, public key published in DNS. The example service provides a signature testing tool at exampleservice.domainconnect.org. I tested our implementation against it before we went live.

The thing I want to emphasize to any developer looking at this: the template repository is not your concern. Templates are an operational concern for whoever runs your platform. Your job is to implement the protocol correctly, so that any valid template can be applied correctly. We tested against the two example service templates — one unsigned, one signed — and those covered essentially the entire surface of the synchronous flow.

End-to-end, from first reading the spec to a working implementation in a staging environment, took our small team about six weeks. Deployment and internal testing took another two. That's the scope.

The thing I hadn't expected: once the infrastructure is in place, adding a new service provider is not a development task. It's a template deployment and review process. The ratio of ongoing maintenance to initial build is very favorable.

---

*Back to: [Storytelling Index](../14_Storytelling.md)*
