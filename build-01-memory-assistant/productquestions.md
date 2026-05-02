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
