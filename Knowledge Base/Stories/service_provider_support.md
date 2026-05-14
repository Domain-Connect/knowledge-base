# Service Provider Support Manager — "They were blaming us for a problem we didn't cause"

*Part of the [Domain Connect Storytelling](../14_Storytelling.md) collection*

---

DNS configuration support was the most thankless category in my queue. Not because the issues were technically hard — they usually weren't. But because the dynamics were uniquely frustrating on both sides.

The customer is angry. They signed up for our service. They followed our instructions. Their email still doesn't work. From their perspective, we're the problem. But when I look at the ticket, the issue is almost always in their DNS zone — a record they entered wrong, a record they didn't enter at all, a conflict with something already in their zone. The problem is at their registrar, not at our service.

And the registrar's support team, when the customer calls them, will often say: this is your service provider's instructions, you need to call them. So the customer bounces between us. Nobody owns the problem. The customer churns.

We had registrar-specific documentation for the major providers. My team maintained it. When a registrar updated their UI — which happens without warning — our documentation was wrong until someone noticed and we updated it. During that window, every customer using that registrar and following our instructions was going to fail. We couldn't fix it proactively because we didn't know when the registrar made a change.

We also had the per-error ticket categories. Wrong MX priority. Missing trailing dot on CNAME. TXT record entered as two separate records instead of one. Verification token expired because setup took too long. Each of these was a distinct ticket type with a distinct resolution path. My team knew all of them. That's not a sign of good operations — that's a sign of a system that forces humans to compensate for structural defects.

When we deployed Domain Connect, I watched what happened to those ticket categories.

The "wrong value" tickets disappeared almost entirely for DNS providers that had deployed our template. Variable substitution is handled by the system — the customer doesn't type values, so they can't type them wrong. The "missing record" tickets disappeared too — the template applies the full record set atomically. The "conflict with existing record" tickets shrank, because the consent flow detects and surfaces conflicts before applying changes.

What remained were tickets from customers whose DNS provider hadn't deployed our template yet, and tickets from customers who had started setup manually before realizing Domain Connect was available. That second category told me something interesting: customers who discovered Domain Connect mid-failure and switched to it generally succeeded. The problem really was the manual process.

The support economics changed in a way I hadn't fully modeled in advance. DNS configuration tickets are expensive not just because of the volume, but because of the time-to-resolution. You have to wait for DNS propagation to verify a fix. With Domain Connect, the record is applied correctly on the first attempt, and there's nothing to resolve.

My team now spends its DNS-related time on genuinely complex issues: DNSSEC configuration, nameserver migration, zone delegation problems. The copy-paste error category, which was large and expensive, is essentially gone for the providers we've onboarded.

---

*Back to: [Storytelling Index](../14_Storytelling.md)*
