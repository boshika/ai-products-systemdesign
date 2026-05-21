"""Render the four system-design diagrams as PNGs.

Architecture diagrams use graphviz (dot) for clean flowchart layout.
Sequence diagrams use matplotlib for full control over lifelines and arrows.

Outputs:
    diagrams/aws-architecture.png
    diagrams/aws-sequence.png
    diagrams/gcp-architecture.png
    diagrams/gcp-sequence.png
"""

import os
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = Path(__file__).parent
HERE.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Architecture diagrams — Graphviz dot
# ---------------------------------------------------------------------------

AWS_ARCH_DOT = r"""
digraph aws {
    rankdir=LR;
    fontname="Helvetica";
    node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=10, margin="0.15,0.08"];
    edge [fontname="Helvetica", fontsize=9, color="#555555"];
    bgcolor="white";
    compound=true;

    subgraph cluster_m365 {
        label="Microsoft 365 tenant";
        style="rounded,filled";
        fillcolor="#eaf3ff";
        color="#9bbcde";
        SP  [label="SharePoint Online", fillcolor="#cfe2f3"];
        GR  [label="MS Graph API",      fillcolor="#cfe2f3"];
        AAD [label="Entra ID / AAD",    fillcolor="#cfe2f3"];
        SP -> GR [dir=none];
        AAD -> GR [dir=none];
    }

    subgraph cluster_ingest {
        label="Ingestion plane (AWS)";
        style="rounded,filled";
        fillcolor="#fff4e6";
        color="#e0b070";
        WH  [label="API Gateway\nGraph webhook receiver", fillcolor="#ffe2bd"];
        EB  [label="EventBridge bus\nsharepoint.events", fillcolor="#ffe2bd"];
        Q1  [label="SQS: change-queue\nFIFO per siteId",  fillcolor="#ffe2bd"];
        F1  [label="Lambda: delta-poller\nscheduled + on-demand", fillcolor="#ffe2bd"];
        F2  [label="Lambda: fetch-doc\n+ ACL resolver", fillcolor="#ffe2bd"];
        S3R [label="S3: raw-docs\nversioned, KMS", fillcolor="#ffe2bd"];
        DDB [label="DynamoDB:\ndoc-state, acl-cache", fillcolor="#ffe2bd"];
    }

    subgraph cluster_proc {
        label="Processing plane";
        style="rounded,filled";
        fillcolor="#e8f5e9";
        color="#8bbf8b";
        SF  [label="Step Functions\nprocess-doc workflow", fillcolor="#cfe9d2"];
        EX  [label="Lambda/ECS: extract\nTextract for PDF/img", fillcolor="#cfe9d2"];
        CH  [label="ECS: chunker\nstructure-aware", fillcolor="#cfe9d2"];
        EM  [label="Bedrock: Titan/Cohere\nembeddings", fillcolor="#cfe9d2"];
        S3C [label="S3: chunks +\nmetadata", fillcolor="#cfe9d2"];
    }

    subgraph cluster_index {
        label="Indexing + retrieval";
        style="rounded,filled";
        fillcolor="#f3e8ff";
        color="#b48fcf";
        OS  [label="OpenSearch Serverless\nvector + ACL filter", shape=cylinder, fillcolor="#e3d2f0"];
        EC  [label="ElastiCache Redis\ngroup expansion cache", fillcolor="#e3d2f0"];
    }

    subgraph cluster_query {
        label="Query plane";
        style="rounded,filled";
        fillcolor="#fde7e9";
        color="#d29097";
        APP   [label="App / Copilot UI", fillcolor="#f7c8cd"];
        APIGW [label="API Gateway +\nCognito",     fillcolor="#f7c8cd"];
        ORCH  [label="Lambda:\nquery orchestrator", fillcolor="#f7c8cd"];
        RR    [label="Bedrock: reranker",          fillcolor="#f7c8cd"];
        LLM   [label="Bedrock: Claude / Nova",     fillcolor="#f7c8cd"];
    }

    GR  -> WH  [label="change\nnotifications"];
    WH  -> EB;
    EB  -> Q1;
    Q1  -> F1;
    F1  -> F2;
    F2  -> S3R;
    F2  -> DDB;
    F2  -> SF;
    SF  -> EX -> CH -> EM -> S3C -> OS;

    APP   -> APIGW;
    APIGW -> ORCH;
    ORCH  -> GR    [label="resolve\nprincipals"];
    ORCH  -> EC    [label="cache"];
    ORCH  -> OS    [label="ACL-filtered\nkNN"];
    ORCH  -> RR;
    RR    -> LLM;
    LLM   -> APP   [style=dashed, label="answer"];
}
"""

GCP_ARCH_DOT = r"""
digraph gcp {
    rankdir=LR;
    fontname="Helvetica";
    node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=10, margin="0.15,0.08"];
    edge [fontname="Helvetica", fontsize=9, color="#555555"];
    bgcolor="white";
    compound=true;

    subgraph cluster_m365 {
        label="Microsoft 365 tenant";
        style="rounded,filled";
        fillcolor="#eaf3ff";
        color="#9bbcde";
        SP  [label="SharePoint Online", fillcolor="#cfe2f3"];
        GR  [label="MS Graph API",      fillcolor="#cfe2f3"];
        AAD [label="Entra ID / AAD",    fillcolor="#cfe2f3"];
        SP -> GR [dir=none];
        AAD -> GR [dir=none];
    }

    subgraph cluster_ingest {
        label="Ingestion plane (GCP)";
        style="rounded,filled";
        fillcolor="#fff4e6";
        color="#e0b070";
        LB  [label="HTTPS LB +\nCloud Run: webhook receiver", fillcolor="#ffe2bd"];
        PS  [label="Pub/Sub:\nsharepoint-events\nordered by siteId", fillcolor="#ffe2bd"];
        SCH [label="Cloud Scheduler\n+ delta-poller job", fillcolor="#ffe2bd"];
        CR1 [label="Cloud Run: fetch-doc\n+ ACL resolver", fillcolor="#ffe2bd"];
        GCS [label="GCS: raw-docs\nversioned, CMEK", fillcolor="#ffe2bd"];
        FS  [label="Firestore:\ndoc-state, acl-cache", fillcolor="#ffe2bd"];
    }

    subgraph cluster_proc {
        label="Processing plane";
        style="rounded,filled";
        fillcolor="#e8f5e9";
        color="#8bbf8b";
        WF  [label="Workflows\nprocess-doc orchestration", fillcolor="#cfe9d2"];
        DF  [label="Dataflow / Cloud Run:\nextract + chunk", fillcolor="#cfe9d2"];
        DAI [label="Document AI\nfor PDFs / scans", fillcolor="#cfe9d2"];
        EMB [label="Vertex AI:\ntext-embedding-005", fillcolor="#cfe9d2"];
        GCS2[label="GCS: chunks +\nmetadata", fillcolor="#cfe9d2"];
    }

    subgraph cluster_index {
        label="Indexing + retrieval";
        style="rounded,filled";
        fillcolor="#f3e8ff";
        color="#b48fcf";
        VS  [label="Vertex AI Vector Search\n+ Firestore ACL join", shape=cylinder, fillcolor="#e3d2f0"];
        MEM [label="Memorystore Redis\ngroup expansion cache", fillcolor="#e3d2f0"];
        BQ  [label="BigQuery:\naudit + analytics", fillcolor="#e3d2f0"];
    }

    subgraph cluster_query {
        label="Query plane";
        style="rounded,filled";
        fillcolor="#fde7e9";
        color="#d29097";
        APP   [label="App / Copilot UI", fillcolor="#f7c8cd"];
        APIGW [label="API Gateway +\nIAP / Cloud Identity", fillcolor="#f7c8cd"];
        ORCH  [label="Cloud Run:\nquery orchestrator", fillcolor="#f7c8cd"];
        RR    [label="Vertex AI: reranker", fillcolor="#f7c8cd"];
        LLM   [label="Vertex AI:\nGemini / Claude on Vertex", fillcolor="#f7c8cd"];
    }

    GR  -> LB  [label="change\nnotifications"];
    LB  -> PS;
    PS  -> CR1;
    SCH -> CR1;
    CR1 -> GCS;
    CR1 -> FS;
    CR1 -> WF;
    WF  -> DF  -> DAI;
    DF  -> EMB -> GCS2 -> VS;

    APP   -> APIGW;
    APIGW -> ORCH;
    ORCH  -> GR    [label="resolve\nprincipals"];
    ORCH  -> MEM   [label="cache"];
    ORCH  -> VS    [label="ACL-filtered\nANN"];
    ORCH  -> FS    [label="ACL verify"];
    ORCH  -> RR;
    RR    -> LLM;
    LLM   -> APP   [style=dashed, label="answer"];
    ORCH  -> BQ    [style=dotted, label="audit"];
}
"""


def render_dot(dot_source: str, out_path: Path) -> None:
    """Render a graphviz dot source to PNG via the dot CLI."""
    p = subprocess.run(
        ["dot", "-Tpng", "-Gdpi=160", "-o", str(out_path)],
        input=dot_source.encode("utf-8"),
        check=True,
        capture_output=True,
    )
    print(f"  wrote {out_path}  ({out_path.stat().st_size} bytes)")


# ---------------------------------------------------------------------------
# Sequence diagrams — matplotlib
# ---------------------------------------------------------------------------

def render_sequence(
    title: str,
    actors: list[tuple[str, str]],
    events: list[tuple[str, str, str, str]],
    out_path: Path,
    notes: list[tuple[int, str]] | None = None,
) -> None:
    """Draw a sequence diagram.

    actors: list of (id, label) tuples in horizontal order.
    events: list of (from_id, to_id, label, style) tuples where style is
            'sync' (solid), 'reply' (dashed), or 'self' (loop).
    notes:  list of (event_index, note_text) for "alt" annotations.
    """
    n_actors = len(actors)
    n_events = len(events)

    fig_w = max(13, n_actors * 1.8)
    fig_h = max(7, n_events * 0.55 + 2)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=160)
    ax.set_xlim(0, n_actors + 1)
    ax.set_ylim(-(n_events + 2), 1.5)
    ax.axis("off")

    # Actor positions
    actor_x = {a_id: i + 0.5 for i, (a_id, _) in enumerate(actors)}
    actor_palette = [
        "#cfe2f3", "#ffe2bd", "#cfe9d2", "#e3d2f0", "#f7c8cd",
        "#fff2cc", "#d9d9f3", "#d9ead3", "#fce5cd",
    ]

    # Actor boxes + lifelines
    for i, (a_id, label) in enumerate(actors):
        x = actor_x[a_id]
        color = actor_palette[i % len(actor_palette)]
        box = FancyBboxPatch(
            (x - 0.42, 0.4), 0.84, 0.7,
            boxstyle="round,pad=0.04",
            linewidth=1.2, edgecolor="#333333", facecolor=color,
        )
        ax.add_patch(box)
        ax.text(x, 0.75, label, ha="center", va="center", fontsize=9.5, weight="bold")
        # Lifeline
        ax.plot(
            [x, x], [0.4, -(n_events + 1)],
            linestyle=(0, (4, 4)), color="#999999", linewidth=0.9, zorder=1,
        )

    # Events
    for i, (src, dst, text, style) in enumerate(events):
        y = -(i + 0.5)
        x1 = actor_x[src]
        x2 = actor_x[dst]

        if style == "self":
            # Self-loop: small rectangle to the right
            ax.annotate(
                "", xy=(x1 + 0.4, y - 0.25), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-", color="#333", lw=1),
            )
            ax.annotate(
                "", xy=(x1, y - 0.25), xytext=(x1 + 0.4, y - 0.25),
                arrowprops=dict(arrowstyle="->", color="#333", lw=1),
            )
            ax.text(x1 + 0.05, y - 0.05, text, fontsize=8.5, va="bottom", ha="left")
            continue

        ls = "-" if style == "sync" else (0, (5, 3))
        arrow = FancyArrowPatch(
            (x1, y), (x2, y),
            arrowstyle="->",
            mutation_scale=14,
            linewidth=1.2,
            color="#222222",
            linestyle=ls,
            zorder=3,
        )
        ax.add_patch(arrow)

        mx = (x1 + x2) / 2
        ax.text(
            mx, y + 0.18, text,
            fontsize=8.5, ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.85),
        )

    # Notes (e.g. "alt cache miss")
    if notes:
        for idx, note in notes:
            y = -(idx + 0.45)
            ax.text(
                0.05, y, note,
                fontsize=8.5, style="italic", color="#666666",
                ha="left", va="center",
            )

    ax.set_title(title, fontsize=12, weight="bold", pad=14)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  wrote {out_path}  ({out_path.stat().st_size} bytes)")


# ---------------------------------------------------------------------------
# AWS sequence content
# ---------------------------------------------------------------------------

AWS_ACTORS = [
    ("U",   "User\n(browser)"),
    ("API", "API GW +\nCognito"),
    ("Q",   "Query\nOrchestrator"),
    ("G",   "MS Graph"),
    ("R",   "Redis\n(ACL cache)"),
    ("OS",  "OpenSearch"),
    ("RR",  "Reranker\n(Bedrock)"),
    ("LLM", "Claude\n(Bedrock)"),
]

AWS_EVENTS = [
    ("U",   "API", "question + OBO token",                                  "sync"),
    ("API", "Q",   "authenticated request",                                 "sync"),
    ("Q",   "R",   "get principals(userOid)",                               "sync"),
    ("Q",   "G",   "[cache miss] transitiveMemberOf(userOid)",              "sync"),
    ("G",   "Q",   "groups + tenant principals",                            "reply"),
    ("Q",   "R",   "set principals (TTL 10m)",                              "sync"),
    ("Q",   "Q",   "embed(query) via Bedrock",                              "self"),
    ("Q",   "OS",  "kNN search + filter: allowed_principals ∩ user + tenant_id", "sync"),
    ("OS",  "Q",   "top-50 candidates",                                     "reply"),
    ("Q",   "G",   "bulk permission re-check on top-K docIds",              "sync"),
    ("G",   "Q",   "confirmed-accessible subset",                           "reply"),
    ("Q",   "RR",  "rerank(query, confirmed candidates)",                   "sync"),
    ("RR",  "Q",   "top-8 chunks",                                          "reply"),
    ("Q",   "LLM", "prompt(question, top-8 with citations)",                "sync"),
    ("LLM", "Q",   "grounded answer + citation map",                        "reply"),
    ("Q",   "API", "answer + source links (only docs user can open)",      "reply"),
    ("API", "U",   "response",                                              "reply"),
]

# ---------------------------------------------------------------------------
# GCP sequence content
# ---------------------------------------------------------------------------

GCP_ACTORS = [
    ("U",   "User\n(browser)"),
    ("API", "API GW +\nIAP"),
    ("Q",   "Query\nOrchestrator\n(Cloud Run)"),
    ("G",   "MS Graph"),
    ("R",   "Memorystore\nRedis"),
    ("V",   "Vector\nSearch"),
    ("F",   "Firestore\n(chunks+ACL)"),
    ("RR",  "Reranker\n(Vertex)"),
    ("LLM", "Gemini\n(Vertex)"),
]

GCP_EVENTS = [
    ("U",   "API", "question + OBO token",                                  "sync"),
    ("API", "Q",   "authenticated request",                                 "sync"),
    ("Q",   "R",   "get principals(userOid)",                               "sync"),
    ("Q",   "G",   "[cache miss] transitiveMemberOf(userOid)",              "sync"),
    ("G",   "Q",   "groups + tenant principals",                            "reply"),
    ("Q",   "R",   "set principals (TTL 10m)",                              "sync"),
    ("Q",   "Q",   "embed(query) via Vertex",                               "self"),
    ("Q",   "V",   "ANN + restricts: tenant_id & allowed_principals",       "sync"),
    ("V",   "Q",   "top-50 chunkIds + scores",                              "reply"),
    ("Q",   "F",   "batch-get chunks + per-chunk ACL",                      "sync"),
    ("F",   "Q",   "content + ACL JSON",                                    "reply"),
    ("Q",   "G",   "bulk permission re-check on top-K docIds",              "sync"),
    ("G",   "Q",   "confirmed-accessible subset",                           "reply"),
    ("Q",   "RR",  "rerank(query, confirmed candidates)",                   "sync"),
    ("RR",  "Q",   "top-8 chunks",                                          "reply"),
    ("Q",   "LLM", "prompt(question, top-8 with citations)",                "sync"),
    ("LLM", "Q",   "grounded answer + citation map",                        "reply"),
    ("Q",   "API", "answer + source links",                                 "reply"),
    ("API", "U",   "response",                                              "reply"),
]


def main() -> None:
    print("Rendering architecture diagrams (graphviz)...")
    render_dot(AWS_ARCH_DOT, HERE / "aws-architecture.png")
    render_dot(GCP_ARCH_DOT, HERE / "gcp-architecture.png")

    print("Rendering sequence diagrams (matplotlib)...")
    render_sequence(
        "AWS — Query-time ACL-enforced retrieval",
        AWS_ACTORS, AWS_EVENTS,
        HERE / "aws-sequence.png",
    )
    render_sequence(
        "GCP — Query-time ACL-enforced retrieval",
        GCP_ACTORS, GCP_EVENTS,
        HERE / "gcp-sequence.png",
    )
    print("Done.")


if __name__ == "__main__":
    main()
