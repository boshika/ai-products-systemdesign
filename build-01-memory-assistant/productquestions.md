# Product Questions — Build 1: Memory Assistant

---

## 1. Memory boundary transparency

**Does your user know when the system has forgotten something they said earlier, and if so, how does the product communicate that without breaking their trust?**

We embed a context meter in the chat UI that shows turn count in plain language, shifts from green to amber to red as the window fills, and surfaces a pin prompt on individual messages before they fall out of the window. The user always knows what the system is holding and has a clear action to take before anything is lost.

---

## 2. Strategy-to-tier mapping

**Which memory strategy — sliding window, summarization, or token budget — maps to which user tier, and what is the unit economics justification for each?**

| Strategy | Tier | Unit economics |
|---|---|---|
| **Sliding Window** | Free | Fixed window (e.g. 4 turns) = N tokens per call = X cents per 100 conversations. Predictable and cheap. |
| **Summarization** | Paid | Adds a periodic compression call, amortised across turns rather than charged per message. More expensive than window but predictably so — right for users who need longer memory. |
| **Token Budget** | Enterprise | Customer sets the token ceiling explicitly. Gives them direct cost control and lets them encode limits into their contract. |


## 3. Who owns what strategy

**What is the explicit list of facts your product guarantees to remember across sessions, and who owns the decision when that list needs to change?**

This is a multi-dimensional question. It has to be answered from different viewpoints — the user, stakeholders, and compliance and privacy.
The user expects a frictionless experience. They would expect to leave the conversation and pick back up with the same context they left — much like how iMessage syncs your full conversation history across devices invisibly. You pick up a new iPhone and everything is there. You never think about the mechanism, you just feel the continuity. That is the experience bar your product needs to meet.
What Apple got right that most products don't is the separation of sync from access. iMessage stores your data in order to return it to you, not in order to read it. Your messages are end-to-end encrypted — Apple is in the middle but cannot read the content. Deletion is user-controlled and permanent. That is the gold standard for how pinned user facts should behave in a stateful chat product — owned by the user, deletable on demand, invisible in operation.
Stakeholders expect to track and document user data to better understand the user. That ambition is legitimate but it needs to stay within the bounds of compliance frameworks like GDPR and CCPA. The critical distinction is whether data flows toward the business or back to the user. iMessage flows data back to the user. Most enterprise products flow it toward the business. A well-designed product finds a way to serve both without violating either.
When user experience and data ambitions conflict with compliance requirements, compliance is non-negotiable — but the PM's job is to design consent and transparency mechanisms that honour all three without making the user feel the friction.

## 4. failure modes and resilience

**When the memory strategy silently fails — a summarizer compresses away a critical user preference, or a window drops an important early turn — how does your product detect it, and what is the recovery path for the user?**

There are two scenariois to define 1. During a single session memmory drop 2. Between sessions memory drop.
For scenario 1. log that capture summarization lengths can be useful. In this case if we are expecting summarization to be say 260 tokens, but it is less than that, then we can log and capture that as a anomlous event in Cloudwatch(from Lambda). Also the pin feature on the UI, captures important user information that is added to the persistent memory in DynamoDB, this layer does not rely on summarization. 
For scenario 2. is a integrity issues in the persistent layer, that means DyanmoDB does not contain information needed for consistency between sessions. In this case, better to state what is known, and prompt the user to re-enter any information that was missed. Also re-pinning this new information might help as well, in restoring and/or adding relevant information. One solution could be, prompting the user to re-pin important information prior to reaching session limit.
