# Service Provider Product Manager — "We were measuring the wrong thing"

*Part of the [Domain Connect Storytelling](../14_Storytelling.md) collection*

---

We had what looked like a healthy activation funnel. Domain setup step: 60% completion. That's industry-acceptable, or so I'd told myself.

Then I started looking at what happened downstream. Customers who completed DNS setup had 90-day retention rates significantly higher than customers who didn't. The delta was larger than I expected. I'd been treating DNS setup completion as a vanity metric — "nice to have" — rather than as a leading indicator of retention.

So I looked harder at the 40% who were dropping off.

Some of them abandoned because they decided the service wasn't right for them — fair. But a meaningful cohort were coming back. They were opening support tickets. They were emailing us saying their email wasn't working, or their website wasn't loading. When we traced those tickets back, they fell into two categories: people who had given up on DNS setup entirely, and people who had completed it incorrectly.

We had registrar-specific DNS documentation for the major providers. It was maintained by a technical writer and updated whenever we heard that something had changed. In practice, it was always at least slightly out of date for at least some registrars, because registrar UIs change and we don't learn about it until users start failing.

A colleague forwarded me a conversation from the Domain Connect Slack channel. I started reading.

The model is: we write a template once, defining exactly which DNS records our service needs. We sign apply URLs so the parameters can't be tampered with in transit. The DNS provider — which the user already trusts, because it's where their domain lives — reviews the template, deploys it, and presents a consent screen. The user clicks approve. The records are written correctly, every time.

No registrar-specific documentation. No user transcription errors. No ambiguity about field names or trailing dots.

The activation curve after we implemented Domain Connect was notable. For DNS providers that had deployed our template, completion rates went up significantly. The support tickets in the "DNS setup" category, for those providers, dropped. The users who went through the Domain Connect flow were activating cleanly and not coming back with DNS-related support issues.

The implementation on our side was a few weeks of engineering work: write the template (we based it on an existing similar service's template in the public repository), implement URL signing, add the discovery flow in our onboarding. The ongoing effort is contacting DNS providers to get our template deployed — which is mostly relationship management, not technical work.

The strategic reframe for me was this: we had been optimizing our DNS documentation. We should have been trying to eliminate the need for it. Domain Connect is not a documentation strategy. It's an architecture decision — move the complexity to where it belongs, away from the user.

---

*Back to: [Storytelling Index](../14_Storytelling.md)*
