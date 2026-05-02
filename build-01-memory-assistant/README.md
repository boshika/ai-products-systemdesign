# Build 1 — Multi-Turn Memory Assistant Lab

**Build Days: Saturday · Build 1 of 5**

Based on what we built in the lab, here are the three techniques:

**1. Sliding Window**
You keep only the last N turns of conversation and drop everything older. It's the simplest approach — predictable and cheap — but it has a hard cliff. The moment a fact scrolls out of the window, the model has no memory of it at all. Good for short, task-focused sessions where early context doesn't matter.

**2. Summarization**
Instead of dropping old turns entirely, you compress them into a rolling summary and pass that summary as context alongside recent turns. This extends the effective memory range significantly, but it's lossy — nuance and specifics tend to evaporate in compression. "The user is allergic to shellfish" can become "dietary restrictions noted," which is useless. The quality of this strategy lives or dies on how well you design the summarizer prompt.

**3. Token Budget**
You walk backwards through the conversation history and include turns until you hit a token ceiling, then stop. This is the most faithful to how real model limits actually work — you're reasoning directly about cost rather than turn count. The tradeoff is that the cutoff point is less predictable than a window, and at low budgets it behaves similarly to a small sliding window anyway.

The deeper insight across all three is that none of them are a substitute for persistent storage. Facts that must never be forgotten — user preferences, names, critical context — should live in a database and be injected into every session explicitly, not left to float in the context window and eventually fall off.

---

A browser-based lab for exploring how different memory strategies affect long-running conversations with Claude. No build step, no framework, no dependencies — one HTML file.

---

## What this is

Large language models are stateless. Every API call starts from scratch. To give users the feeling of a continuous conversation, you have to explicitly manage what gets passed back into the context window on each turn.

This lab implements and compares three strategies for doing that:

| Strategy | How it works | Tradeoff |
|---|---|---|
| **Sliding Window** | Keep the last N turns, drop everything older | Simple and predictable — but old facts fall off a hard cliff |
| **Summarization** | Compress older turns into a rolling summary, keep recent turns verbatim | Extends effective memory — but nuance and specifics get lossy |
| **Token Budget** | Walk backwards through history, include turns until you hit a token ceiling | Most faithful to real model limits — but cutoff point is unpredictable |

---

## Features

- **Live chat** — switch strategies mid-conversation and feel the difference immediately
- **20-turn degradation experiment** — injects a seed fact at turn 1, runs filler conversation, probes recall every 4 turns, scores Hit / Partial / Miss across all three strategies in parallel
- **Context usage meter** — live token estimate and fill bar as the conversation grows
- **Memory event log** — shows exactly when turns are dropped, summaries are created, or budget is exhausted
- **PM Story tab** — written analysis of what context window management teaches about product constraints

---

## Quickstart

### Option 1 — open directly in browser

```bash
open memory-assistant-lab.html
```

Most browsers will run it locally without a server. If the API call is blocked by CORS policy, use option 2.

### Option 2 — static server

```bash
# Node
npx serve .

# Python
python3 -m http.server 8080
```

Then open `http://localhost:8080/memory-assistant-lab.html`.

### API key

Paste your Anthropic API key into the key field in the top-right corner of the UI, or hardcode it in the `CONFIG` block at the top of the script:

```js
const CONFIG = {
  apiKey: 'sk-ant-...',   // ← paste here for local dev
  model:  'claude-sonnet-4-20250514',
  ...
};
```

> **Never commit a real API key.** The `CONFIG.apiKey` field is intentionally left blank in the repo. Use the UI input or an environment variable if you serve this from a backend.

---

## Running the experiment

1. Open the **Experiment** tab
2. Adjust window size and token budget sliders in the sidebar if desired
3. Click **run_experiment() ↗**
4. The lab runs 20 turns simultaneously across all three strategies and streams results as they arrive
5. Final scores show how many of the 5 recall probes each strategy got right

**What to look for:**

- Sliding Window with a small window size (2–3 turns) will miss early; increase window size and it holds longer but costs more tokens per call
- Summarization preserves the seed fact better than window when the summary injection is explicit — but degrades when the summary is vague
- Token Budget behaves like a larger sliding window at low budgets; at high budgets it approaches full history

---

## Repo structure

```
ai-products-systemdesign/
    build-01-memory-assistant/
      memory-assistant-lab.html   # full app — single file
      README.md                   # this file
```

---

## Connecting to AWS Bedrock

The lab calls the Anthropic API directly from the browser. To replicate this with **AWS Bedrock + boto3** in Python:

```python
import boto3
import json

client = boto3.client('bedrock-runtime', region_name='us-east-1')

def call_claude(messages: list[dict], system: str, max_tokens: int = 300) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "system": system,
        "messages": messages,
    }
    response = client.invoke_model(
        modelId="anthropic.claude-sonnet-4-5",
        body=json.dumps(body),
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
```

For **token-by-token streaming** on Bedrock:

```python
def call_claude_streaming(messages: list[dict], system: str) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "system": system,
        "messages": messages,
    }
    response = client.invoke_model_with_response_stream(
        modelId="anthropic.claude-sonnet-4-5",
        body=json.dumps(body),
    )
    full_reply = ""
    for event in response["body"]:
        chunk = json.loads(event["chunk"]["bytes"])
        if chunk.get("type") == "content_block_delta":
            token = chunk["delta"].get("text", "")
            print(token, end="", flush=True)
            full_reply += token
    return full_reply
```

The three memory strategies map directly — `buildMessages()` in the JS becomes a Python function that takes `history: list[dict]` and returns a trimmed list to pass as `messages`.

---

## Key PM insight

Context window management forces you to make explicit what your product implicitly promises to remember. The gap between what users expect the system to know and what the context window actually contains is where trust breaks.

Three questions every PM should answer before shipping a conversational feature:

1. **What is your must-never-forget set?** Names, allergies, preferences, account state — these belong in a persistent store, not the context window.
2. **Does your user know where the memory boundary is?** If not, they will blame the product, not the constraint.
3. **Have you run a degradation test?** Ship the experiment, not just the feature.

---

## Model

`claude-sonnet-4-20250514` — update the `CONFIG.model` string to switch models. All Claude 3+ models use the same message format.

---

## License

MIT — use freely, attribution appreciated.
