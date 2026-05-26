# ai-products-systemdesign

System design notes and resources for **AI / ML products** — covering RAG pipelines, LLM application architecture, ML infrastructure, and AI platform design.

> **Companion repo:** [product-interview-vault](https://github.com/boshika/product-interview-vault) covers the PM interview framing for these same topics — product strategy, metrics, behavioral stories, and interview answers. Use both together: this repo for technical depth and architecture, that repo for the PM lens and how to articulate it in interviews.

---

## How to Use These Repos Together

| Topic | Technical depth (here) | PM interview framing |
|-------|------------------------|----------------------|
| RAG and knowledge systems | `rag_system_design/`, `systemdesign/week-02` | [AI-Technical/rag-and-knowledge-systems.md](https://github.com/boshika/product-interview-vault/blob/main/AI-Technical/rag-and-knowledge-systems.md) |
| Agents and orchestration | `systemdesign/week-03` | [AI-Technical/agents-and-orchestration.md](https://github.com/boshika/product-interview-vault/blob/main/AI-Technical/agents-and-orchestration.md) |
| Evaluation and quality | `systemdesign/week-06` | [AI-Technical/evaluation-and-quality.md](https://github.com/boshika/product-interview-vault/blob/main/AI-Technical/evaluation-and-quality.md) |
| Model selection and cost | `systemdesign/week-05` | [AI-Technical/model-selection-and-cost.md](https://github.com/boshika/product-interview-vault/blob/main/AI-Technical/model-selection-and-cost.md) |
| AI platform architecture | `systemdesign/week-05` | [Strategy/ai-product-strategy.md](https://github.com/boshika/product-interview-vault/blob/main/Strategy/ai-product-strategy.md) |
| Safety and governance | `systemdesign/week-06` | [AI-Technical/safety-and-governance.md](https://github.com/boshika/product-interview-vault/blob/main/AI-Technical/safety-and-governance.md) |
| Control plane build | `build-01-memory-assistant/` | [Strategy/Control-Plane-Story.md](https://github.com/boshika/product-interview-vault/blob/main/Strategy/Control-Plane-Story.md) |
| System design capstone | `systemdesign/week-08` | [weekly/week-08-integration-and-capstone.md](https://github.com/boshika/product-interview-vault/blob/main/weekly/week-08-integration-and-capstone.md) |

---

## Structure

| Folder / File | What's Inside |
|---------------|--------------|
| `systemdesign/` | Weekly course notes (8-week AI system design program) |
| `rag_system_design/` | RAG-specific system design — AWS, GCP, and interview questions |
| `build-01-memory-assistant/` | End-to-end memory assistant build |
| `ai-system-design-course.html` | Self-contained HTML course reference |

---

## Weekly Course Notes

`systemdesign/` contains structured notes from an 8-week AI system design program:

| File | Topic |
|------|-------|
| `week-01-foundations-of-ai-system-design.md` | Foundations of AI system design |
| `week-02-llm-application-architecture.md` | LLM application architecture |
| `week-03-ml-infrastructure-and-model-serving.md` | ML infrastructure and model serving |
| `week-04-data-pipelines-and-feature-engineering.md` | Data pipelines and feature engineering |
| `week-05-ai-platform-architecture.md` | AI platform architecture |
| `week-06-evaluation-and-observability-systems.md` | Evaluation and observability systems |
| `week-07-scalability-reliability-and-cost-optimization.md` | Scalability, reliability, and cost optimization |
| `week-08-system-design-interview-practice-and-capstone.md` | System design interview practice and capstone |

---

## RAG System Design

`rag_system_design/` covers retrieval-augmented generation system design across cloud providers:

| File | Topic |
|------|-------|
| `aws-system-design.md` | RAG system design on AWS |
| `gcp-system-design.md` | RAG system design on GCP |
| `product-questions.md` | Product questions for RAG systems |
| `technical-questions.md` | Technical questions for RAG systems |

---

## Build 01 — Memory Assistant

`build-01-memory-assistant/` is an end-to-end build project:

| File | Description |
|------|-------------|
| `memory-assistant.html` | Interactive memory assistant reference |
| `systemdesign.md` | System design doc for the memory assistant |
| `productquestions.md` | Product questions and considerations |
| `aws_stateful_chat_architecture.svg` | AWS stateful chat architecture diagram |

---

## Course Reference

[`ai-system-design-course.html`](ai-system-design-course.html) is a self-contained HTML course reference covering AI system design concepts.

**To open it locally:**

```bash
open ai-system-design-course.html
```

No server or dependencies needed — fully offline-ready.

---

## Related Repositories

- [product-interview-vault](https://github.com/boshika/product-interview-vault) — PM interview prep: strategy, metrics, behavioral, and AI product framing
- [ai-knowledge-graph](https://github.com/boshika/ai-knowledge-graph) — AI and Cloud concepts knowledge base
