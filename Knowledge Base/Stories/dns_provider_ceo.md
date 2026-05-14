# DNS Provider CEO — "The renewal rate gap nobody was talking about"

*Part of the [Domain Connect Storytelling](../14_Storytelling.md) collection*

---

Every year we get the same renewal data. A percentage of domains drop. You look at the numbers, you assign them to churn models, and you move on. What I didn't understand for a long time was that the churn wasn't primarily about pricing, or competition, or customers deciding they didn't need a domain anymore.

It was about activation.

A CENTR study on domain renewal rates showed something I couldn't unsee once I'd read it. Domains with high content — meaning the customer had actually connected their domain to something and built an online presence — renewed at around 90%. Domains sitting unused renewed at around 70%. Twenty percentage points of renewal probability, determined almost entirely by whether the customer got their domain working.

The gap between "registered" and "working" is DNS configuration. That's the step where half of motivated, paying customers fail. Not because they give up. Because they try, they can't figure out how to create an MX record or a CNAME, they call support, and somewhere in that process — either immediately or at renewal — they disengage.

Our support team had a playbook for Microsoft 365 DNS setup. We'd built it because we were getting thousands of calls. That playbook represented an enormous amount of operational cost that was, in retrospect, a symptom of a structural problem we hadn't named yet.

Domain Connect named it. The protocol exists because the industry built excellent infrastructure for registering domains and resolving them, then left the last step — connecting them to services — as a manual, error-prone task that requires expert knowledge most customers don't have.

When my product team briefed me on implementing Domain Connect, I asked two questions. First: is this a real standard with staying power, or is this something we'll implement and then abandon? The answer was clear — it's been running in production since 2016, the IETF has a working group standardizing it, and GoDaddy, Cloudflare, and IONOS are already live. This is infrastructure, not an experiment.

Second: what's the business case? The answer was the renewal data I already knew, plus a support cost reduction that was immediately measurable, plus a competitive differentiation argument: customers who can connect their domains to services in one click don't have a reason to move to another registrar for a better experience.

We implemented it. The support ticket reduction in DNS configuration was real and fast. The renewal effect takes longer to measure — you need a full renewal cycle — but the leading indicators are there. Customers who go through the Domain Connect flow activate their services. Customers who activate their services stay.

The strategic point I'd make to any CEO in this space is this: the domain industry has optimized heavily for acquisition and for resolution infrastructure. The activation gap in the middle is where we've been losing customers for years. Domain Connect is the most direct fix available, it's already built, and the ecosystem is already there. The question is how quickly you want to close that gap.

---

*Back to: [Storytelling Index](../14_Storytelling.md)*
