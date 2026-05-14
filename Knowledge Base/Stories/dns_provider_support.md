# DNS Provider Support Manager — "When the same ticket arrives a hundred times, that's not a user problem"

*Part of the [Domain Connect Storytelling](../14_Storytelling.md) collection*

---

My team handles tier-1 and tier-2 DNS support. We see everything: propagation delays, DNSSEC misconfigurations, zone transfer failures. Most of it is genuinely complex.

But a significant chunk of my queue, for a long time, was not complex. It was users who had received a list of DNS records from a service provider and couldn't figure out where to enter them. Or had entered them wrong — a trailing dot missing from a CNAME target, an MX priority entered in the wrong field, a TXT record split across two lines when it shouldn't have been.

We'd developed a playbook for the most common services. My agents could walk through Microsoft 365 setup in their sleep. They knew exactly which fields to look for in our control panel, in which order, with which values. That playbook existed because the same set of mistakes kept recurring — not because the mistakes were hard to explain, but because the task was structurally error-prone for non-expert users.

The support cost per ticket is real. So is the time-to-resolution, which for DNS configuration tickets is long because you often can't verify success until records propagate. And so is churn: users who call support once, fail, and call support again tend to have lower retention than users who succeed on the first try.

When we started discussing Domain Connect internally, my immediate question was: what breaks? I've seen enough "solutions" that reduce one category of ticket and create three new categories. I wanted to understand the failure modes.

What I found was that the failure modes were well-defined and largely preventable. The consent screen is shown to the authenticated, verified zone owner. The template is pre-approved — our product team reviews it before deployment. Variable substitution is handled by our system, not the user. The most common class of error in manual setup — wrong value in the wrong field — simply cannot happen in a template-based flow.

After we launched Domain Connect support for the major service providers, I tracked the ticket volume closely. Tickets for Microsoft 365 DNS configuration dropped. The tickets that remained were either from users with domains hosted elsewhere (not our zones), or from users whose service provider wasn't yet using our implementation.

The other thing that changed, which I hadn't fully anticipated, was the nature of escalations. Before Domain Connect, a significant portion of tier-2 escalations were "the records look right but the service still doesn't work" — usually a conflict with an existing record we'd missed during manual review. After, that category shrank substantially. Template conflict detection handles it automatically.

My team still handles complex DNS issues. But we spend less time teaching non-experts how to copy and paste DNS records. That's a better use of their skills.

---

*Back to: [Storytelling Index](../14_Storytelling.md)*
