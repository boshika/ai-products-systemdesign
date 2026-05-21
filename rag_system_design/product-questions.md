# Product Questions — Staff PM, RAG over SharePoint with Entitlements

Questions a Staff-level PM should expect across interview loops, exec reviews, customer escalations, and roadmap defenses for an enterprise RAG product backed by SharePoint with strict entitlement enforcement. Each question includes the *intent behind it* (what the asker is really probing) and a *scaffold for a strong answer* — not a script.

---

## 1. Strategy and positioning

### Q1. Why build this rather than tell customers to use Microsoft Copilot for M365?
**Intent.** Tests whether you understand the competitive frame and can defend a "build" decision against a credible alternative from the platform vendor.
**Answer scaffold.**
- Acknowledge Copilot is the default — that's the hurdle.
- Differentiate on: (a) **cross-source RAG** — SharePoint is rarely standalone; customers want a single answer pane across SharePoint + Confluence + Salesforce + their data lake. Copilot is M365-centric. (b) **Bring-your-own-model and bring-your-own-eval** — regulated industries want to pin a specific model version, run their own evals, and audit retrieval. (c) **Custom entitlement semantics** — many enterprises layer additional access policies (data classification, region restrictions, project-based redaction) on top of SharePoint ACLs. We honor SharePoint ACLs *and* the customer's overlay. (d) **Price/seat economics** at scale for read-mostly populations Copilot's per-seat pricing punishes.
- Be honest about where we lose: deep Outlook/Teams/Office authoring integration. We don't compete there.

### Q2. Who is the buyer, who is the user, and how do their incentives diverge?
**Intent.** Can you articulate a real B2B distinction and design for the gap.
**Answer scaffold.**
- **Buyer:** CIO/CISO/Chief Data Officer — buys on security, auditability, TCO, and one-throat-to-choke across knowledge silos.
- **Champion:** Head of Knowledge / Enablement / IT Productivity — measured on adoption and ticket deflection.
- **End user:** Knowledge worker — measured on getting an answer faster than Slack-pinging a colleague.
- **Divergence:** The buyer wants strict guardrails (no leakage, full audit log, region pinning). The end user wants the system to "just answer" without friction. Product must make the safety story invisible to the end user while being inspectable for the buyer. Concretely: never make the user fight the ACL — if they can't see a source, the assistant says "I can't access that information in your tenant" rather than showing a redaction artifact.

### Q3. What is your wedge — what does V1 do that nothing else does, and what do you cut?
**Intent.** Forces ruthlessness. Staff PMs are evaluated on what they say no to.
**Answer scaffold.**
- **In:** SharePoint Online ingestion via Graph, ACL-faithful retrieval, citation-grounded answers, audit log, golden-eval harness for the customer's domain, three flagship integrations (Slack, Teams, web).
- **Out of V1:** SharePoint on-prem, multi-source federation beyond SharePoint, fine-tuning, agentic write-back to SharePoint, multi-modal (image/video) retrieval.
- **Why those cuts:** SharePoint Online + Graph alone is a credible deliverable in two quarters; the harder enterprise objections (permissions, audit, eval) are all in V1 so the buyer can actually sign. Multi-source is V2 — once we've proven we can do *one* source perfectly, the second is incremental.

### Q4. How does this compete with Glean / Elastic / Coveo / a homegrown LangChain stack?
**Intent.** Are you fluent in the actual market, not the slide-deck market.
**Answer scaffold.**
- **Glean:** strongest direct competitor; broad connector library, good ACL handling. We win on entitlement *depth* (per-chunk ACL stamping plus query-time Graph re-check, not just connector-level ACL) and on customer-owned eval. We lose on time-to-value across many small sources.
- **Elastic / Coveo:** strong on retrieval, weaker on the LLM-grounded answer + audit story; often paired with a separate orchestration layer.
- **Homegrown LangChain:** zero procurement friction but the customer eventually hits the same wall on entitlements, eval, freshness, and cost predictability that justified the buy. Our pitch is "we already solved the part you'd spend two years failing at."

---

## 2. Customer, discovery, and demand

### Q5. How did you size the market and decide it's worth building?
**Intent.** Can you do credible market sizing without hand-waving.
**Answer scaffold.**
- **TAM bound:** Microsoft 365 enterprise seats × % of orgs where SharePoint is the primary knowledge store × willingness-to-pay for AI search overlay. Triangulate top-down (industry analyst seat counts) and bottom-up (named-account ACV × addressable accounts).
- **SAM:** subset where (a) data sovereignty rules permit cloud RAG, (b) SharePoint is materially used, (c) buyer maturity supports adding an AI overlay budget line.
- **SOM (Y1):** ~50 design partners → 10 paid → $X ACV at $Y average. State your number and your confidence interval. The interviewer cares more about your reasoning than the exact figure.

### Q6. Walk me through how you'd run discovery for this. Who do you talk to and what do you ask?
**Intent.** Are you a discovery PM or a roadmap-defender PM.
**Answer scaffold.**
- **Cohorts:** 5 companies that bought Glean, 5 that built homegrown, 5 that did neither and are using Copilot only, 5 in regulated industries (finance/health/public sector).
- **Per cohort, three conversations:** the buyer (procurement frame), the champion (rollout frame), 2-3 end users (workflow frame).
- **Questions that matter:** "Walk me through the last time you needed an answer and couldn't find it." "Show me the search you actually used last week." "What would have to be true for you to trust an AI answer with no human in the loop?" "What's your current process for a permission audit?" Avoid leading questions about features.
- **What I'm listening for:** the moment they describe a workaround — that's the wedge. Workarounds are the unit of opportunity.

### Q7. Give me a concrete user story for V1 with measurable success criteria.
**Intent.** Can you write a real story, not a feature.
**Answer scaffold.**
- *"A new sales engineer at Acme joins the EMEA team. On their first week they ask the assistant 'what's our standard response to the security questionnaire question about data residency?' The assistant returns the canonical answer with three citations to SharePoint docs they have access to, in under 4 seconds, and does not surface the previous quarter's draft sitting in a private VP-only folder."*
- **Success criteria:** answered correctly per the customer's golden eval (≥90% on a 200-question set); P95 latency < 5s; zero ACL violations across the 200 questions; user thumbs-up rate ≥ 70% in first month; deflection of ≥ 1 "who knows about X" Slack message per user per week.

### Q8. What does failure look like in the first year and how would you know early?
**Intent.** Pre-mortems separate Staff PMs from Senior PMs.
**Answer scaffold.**
- **Failure mode 1 — low adoption.** Leading indicator: weekly active rate < 15% of provisioned users by week 6. Cause is usually that the answers don't feel better than the customer's current search. Read: invest in retrieval quality, not features.
- **Failure mode 2 — a single ACL incident.** Leading indicator: any non-zero count on the permission-negative eval set, or a single customer-reported leakage. Cause is almost always an ACL-cache freshness gap.
- **Failure mode 3 — procurement stalls in legal/security.** Leading indicator: design-partner contracts taking > 90 days. Cause is usually our SOC2/ISO posture or data residency story. Read: invest in trust artifacts before more features.
- **Failure mode 4 — answers are technically correct but unhelpful.** Citations are right, content is right, but the user wanted a synthesized recommendation not a paragraph quote. Read: rework the prompt + reranking, not the retrieval.

---

## 3. Trust, safety, and the entitlement story

### Q9. A customer's CISO asks: "Prove to me a user can never see content they shouldn't." What do you tell them?
**Intent.** This is the most-asked question on this product. You have to answer it cleanly.
**Answer scaffold.**
- Walk through the **three gates**: (1) ACLs resolved from SharePoint *before* chunking — no chunk is written to the vector store without its source ACL stamped on it; (2) at query time the vector search itself is filtered by the requester's principals — content the user can't see is excluded from the candidate set, not retrieved-then-redacted; (3) a defense-in-depth Graph re-check on the top-K candidates catches the second-edge case where a permission was revoked within the last cache TTL.
- Add the **observability story:** every query is logged with the chunkIds returned; we run a nightly permission-negative eval that explicitly tries to surface forbidden content for known users; failures page on-call. We can give the CISO read access to their tenant's audit log and eval results.
- Add the **failure containment story:** an ACL resolution failure on a single document blocks indexing of that document — it never silently indexes with a missing ACL.
- Close with the honest part: "Revocation has a bounded latency — typically seconds, worst case 10 minutes — driven by Graph's own webhook latency and our cache TTL. We disclose this and let you tune the TTL down if you need to."

### Q10. How do you handle the "sharing link explosion" problem — a doc shared as 'anyone in the org with the link'?
**Intent.** Tests whether you've thought about the messy edges of SharePoint sharing.
**Answer scaffold.**
- Sharing links are resolved at ACL-capture time into a concrete principal set: "anyone with the link in the org" becomes the tenant-wide group, *not* a global "Everyone." Anonymous links are surfaced as a configurable policy — most enterprises choose to exclude anonymously-shared docs from RAG entirely.
- Customer-facing: a dashboard that shows "documents indexed via permissive sharing links" so the CISO can audit and tighten.

### Q11. What do you do when a user asks a question that requires synthesizing across documents they have varying levels of access to?
**Intent.** Tests reasoning about subtle correctness issues.
**Answer scaffold.**
- The model only sees chunks the user is allowed to see, so synthesis is naturally bounded.
- The edge: if the *answer to the question* depends on a chunk the user can't see, the assistant must say "I don't have enough accessible information to answer that" — not silently produce a partial answer that omits the gated content. This is enforced by requiring every claim in the generated answer to be backed by a citation that's in the user's allowed set, and by training the model to refuse rather than hallucinate.
- We measure this on the eval: a "should refuse" set is part of nightly testing.

### Q12. How do you handle confidential or classified information that has additional access rules beyond SharePoint ACLs?
**Intent.** Tests whether you've thought about overlay policies — enterprise reality.
**Answer scaffold.**
- ACLs are the *floor*. We support customer-defined policy overlays evaluated as additional filters: data classification labels (from Purview / MIP), region/residency tags, project-scope tags.
- Concretely: chunks carry both `allowed_principals` and `policy_tags`. The query orchestrator joins the user's allowed-policy set with the chunk's tags and filters before retrieval.
- Common case: a customer pins all docs labeled "Restricted" so they're indexed but only retrievable by users with an explicit policy claim — not just by ACL inheritance.

---

## 4. Metrics, evals, and decision-making

### Q13. What's your North Star metric and why?
**Intent.** Are you measuring outcomes or outputs.
**Answer scaffold.**
- **North Star:** Weekly Successful Queries per Active User, where "successful" is defined per-tenant via their golden eval + thumbs-up rate.
- Why not "queries per user": rewards volume, not value. A user asking the same broken question ten times is a failure.
- Why not just thumbs-up: low signal, biased to people who bother to rate.
- Pair with two guardrails: ACL violation count (must be 0) and P95 latency (must be < target).

### Q14. How do you measure retrieval quality given that "correct" is fuzzy for natural language?
**Intent.** Tests whether you actually understand eval, not just LLM-as-judge buzzwords.
**Answer scaffold.**
- **Per-customer golden set** of 100-300 question-answer pairs hand-curated with their SMEs at onboarding. Refreshed quarterly.
- **Metrics:** recall@k on retrieval (does the right doc make the top-K), answer correctness scored by both LLM-judge and human spot-check, citation precision (does each claim cite a chunk that supports it), permission-negative recall (does the system refuse when it should).
- **Trust but verify the LLM judge:** sample 5% of judgments for human review monthly; calibrate the judge prompt against drift.
- **Don't ship without it.** A customer without a golden set gets a starter set we generate from their corpus and then refine in week 1.

### Q15. A customer says "the answers are wrong." Walk me through how you debug.
**Intent.** Operational instinct.
**Answer scaffold.**
- **Classify the failure first.** Five buckets: retrieval miss (the right doc wasn't retrieved), ranking miss (it was retrieved but not in top-K to the model), generation miss (model had the right context but generated wrong), citation miss (right answer wrong source), permission noise (user thinks an answer is wrong because we filtered the source they expected).
- **Tools:** the audit log gives me the exact chunks served and the model output. I replay against each layer.
- **Most common cause in my experience:** chunking. A good answer was split across two chunks and only one made it into the prompt. Fix: revisit chunk boundaries, increase overlap, or upgrade to structure-aware chunking for that doc type.
- **Tell the customer:** what bucket, what fix, what timeline. Don't hand-wave "we'll look into it."

### Q16. How do you A/B test a RAG system? Embedding-model changes, chunking strategy changes, prompt changes?
**Intent.** Tests whether you've actually shipped an LLM product.
**Answer scaffold.**
- **Offline first.** Every change is run against the per-customer golden set + a shared eval set before any user-facing rollout.
- **Online experiments are tricky** because user behavior is sparse and noisy. We use stratified rollouts (e.g., 10% of one tenant) and measure thumbs-up rate, citation-click-through, regenerate-rate, abandonment.
- **Don't A/B everything online.** Some changes (embedding model swap) require full re-indexing — you A/B at the tenant level, not the query level.
- **Avoid the metric-gaming pitfall:** thumbs-up rate goes up when answers are confident-sounding, even if they're wrong. Always pair with golden-eval correctness.

---

## 5. Prioritization and roadmap

### Q17. Three big customers each ask for a different feature. CFO wants you to focus on revenue. How do you decide?
**Intent.** The classic. Tests prioritization frameworks and political instinct.
**Answer scaffold.**
- Reframe: "feature requests" aren't the unit — *problems blocking expansion or retention* are.
- For each ask: what problem? Who else has it? Is it a "won't renew" problem or a "would be nice" problem? What's the LTV at stake?
- Score on **reach × impact × confidence × strategic fit / cost.**
- Bring the CFO into the framing: "I can name the dollar value of each ask within a week." Then I have a real conversation, not a power struggle.
- Concrete answer for this product: I bias toward whichever ask unblocks the *trust* story (audit features, certifications, residency) because those gate the entire pipeline, not just one customer.

### Q18. What would you cut from V1 if engineering told you you had half the time?
**Intent.** Forces ruthlessness under constraint.
**Answer scaffold.**
- **Cut:** custom branding, deep Slack/Teams integration (web UI only), multi-language UI, anything beyond two file types (PDF + .docx), advanced analytics dashboards.
- **Keep:** the entitlement model (it's the product), the audit log (the buyer), citations (the user trust), golden eval (the operational story).
- The principle: ship the thing that's hard to bolt on later and that defines the product's promise. Anything that's "just engineering" can wait.

### Q19. How do you decide when to charge for this — per seat, per query, per tenant?
**Intent.** Tests commercial thinking, not engineering.
**Answer scaffold.**
- **Per seat** is what enterprise buyers are used to and what their finance teams can model. Default to it.
- **Per query** punishes engagement, which we want to incentivize. Avoid as the primary line.
- **Tier on capabilities** (basic / pro / enterprise: more sources, longer audit retention, dedicated infra, custom eval support). This gives the sales motion something to expand into.
- **Watch usage extremes.** If a tenant's QPS is 10x the median, that's either a heavy power user (good) or an abusive integration loop (bad). Build fair-use limits, not bills that surprise.

### Q20. The CEO wants this in front of customers in 90 days. Is that the right goal?
**Intent.** Do you push back on leadership when the right answer is "no, but here's the alternative."
**Answer scaffold.**
- "Yes — if we define 'in front of customers' as design-partner private preview with 3-5 named accounts, no SLA, weekly feedback loops."
- "No — if we mean GA. The entitlement story and the eval harness are not bluffable; if we ship them broken, we lose the procurement battle for the next year."
- Offer the dated milestones: design-partner kickoff at 30 days, first end-to-end answer at 60, three customers in active eval at 90, GA target six months later. Get the CEO to either accept that or articulate which trade-off they want to make.

---

## 6. Cross-functional and operational

### Q21. How do you work with the security team on this — what's the operating cadence?
**Intent.** Are you going to ship something they have to break, or partner from day one.
**Answer scaffold.**
- Security is a co-author on the entitlement model — they review the chunk schema, the query filter logic, and the audit log spec *before* engineering builds them.
- Standing weekly review of permission-negative eval results.
- A pre-defined incident playbook for ACL violations (customer comms, log preservation, root cause, remediation timeline) — written before we need it.
- Threat modeling at every major architectural change (new source, new model, new policy overlay).

### Q22. Your model provider releases a new embedding model that's 30% better but requires re-indexing every customer. Go or no-go?
**Intent.** Cost vs. quality decision with operational weight.
**Answer scaffold.**
- Decision factors: cost of re-indexing (compute + provider $$) vs. measurable retrieval improvement on customer golden sets (not the vendor's benchmark — ours).
- Ops factors: can we re-index in the background without query downtime? Per-tenant or fleet-wide? Can we roll back?
- Commercial factors: does this enable a new SKU or close a gap with a competitor?
- Default policy: validate on three customers' golden sets, run a controlled migration on one mid-size tenant, then fleet-wide over four weeks if metrics hold. Never a Friday cut-over.

### Q23. How do you scope a beta vs. GA launch for this product?
**Intent.** Operational rigor.
**Answer scaffold.**
- **Beta exit criteria:** at least 5 design partners with >50 weekly active users each, 0 ACL violations in 30 days, P95 latency within target, eval correctness ≥ 85%, customer-reportable audit log live, SOC2 Type II in progress, support runbook tested via game-day.
- **GA additions:** SOC2 Type II complete, documented SLAs, public pricing, billing/metering live, partner ecosystem for at least one major reseller, on-call rotation 24/7.

### Q24. What does your roadmap look like for the year after launch?
**Intent.** Are you thinking past the launch.
**Answer scaffold.**
- **Quarter 1 post-GA:** harden ingestion (edge SharePoint configurations the design partners surface), expand evals, ship the policy-overlay layer.
- **Q2:** second source (Confluence is the typical request) using the same ACL contract, prove the model generalizes.
- **Q3:** agentic actions — go from answering to acting (draft a doc, file a ticket) inside the same entitlement frame. This is where the product becomes sticky.
- **Q4:** offline / air-gapped deployment for regulated customers; bring-your-own-model.
- Through the year: monthly retrieval-quality lifts driven by eval-data flywheel from real usage.

---

## 7. Questions you should expect to ask back

A Staff PM is also judged by what they ask. Good ones to volley back when given the chance:
- "How does this team currently make trade-offs between trust/safety work and feature velocity?"
- "Who owns the eval harness today, and what's the current quality of it?"
- "What's the longest-standing customer complaint about the existing product, if any?"
- "What does the CEO believe is true about this market that you and your peers don't?"
- "When the last big incident happened, what was the post-mortem culture like?"

---

*End of product questions document.*
