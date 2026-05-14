# DNS Provider Product Manager — "The support ticket that changed how I thought about DNS"

*Part of the [Domain Connect Storytelling](../14_Storytelling.md) collection*

---

About two years ago, I was doing a routine support ticket review — the kind of monthly audit where you look for patterns and figure out what's worth engineering time. We have tens of thousands of DNS zones under management, and I expected the usual mix: propagation questions, locked records, billing confusion.

What I found was that DNS configuration tickets for third-party services — Microsoft 365, Google Workspace, Shopify — were not just common. They were the single largest driver of tier-2 escalations. Users who could navigate our control panel fine for everything else were completely stuck when a service sent them instructions like "create an MX record pointing to aspmx.l.google.com with priority 1."

The worst part wasn't the volume. It was reading the actual tickets. These were people who had done everything right. They registered a domain. They signed up for the service. They were motivated, paying customers at the finish line. And they were failing — because the last step required knowledge they had no reason to have.

I started mapping our support cost against specific services. Microsoft 365 alone was responsible for a disproportionate share. We had internal documentation, help articles, video tutorials — all of it. Users still failed at roughly a 50% rate.

That's when a colleague mentioned Domain Connect. I was skeptical at first — protocols don't usually solve UX problems, they usually create new ones. But the model was interesting. The service provider defines a template. We vet it, we deploy it, we build a consent flow. The user never touches a DNS record directly.

I pulled up the template repository. Microsoft 365 had a template. Google Workspace had a template. Shopify had one. 400-something service providers, already written and waiting to be deployed.

We ran the numbers on implementation cost. The API work, the consent screen, the template hosting infrastructure — it was a defined scope. Not trivial, but a one-time investment. After that, each new template is just a deployment decision, not a development project.

Eighteen months later, our Domain Connect flow handles a meaningful percentage of service connections. Support tickets for DNS configuration are down substantially for the services we've onboarded. The tickets that remain are almost all for providers whose templates we haven't deployed yet — which tells me the ceiling is even higher.

The product realization I had was this: we were optimizing the DNS control panel as if our customers' goal was to manage DNS. It isn't. Their goal is to get their service working. Domain Connect aligns what we build with what users actually need to accomplish.

---

*Back to: [Storytelling Index](../14_Storytelling.md)*
