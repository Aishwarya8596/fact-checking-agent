# Session 17: LangGraph Workflow

## What We Are Building

In earlier sessions, our pipeline was normal Python function calls.

In Session 17, we express the same workflow as a LangGraph graph:

```text
decompose_claim -> check_subclaims -> aggregate_verdict -> build_report
```

## Why LangGraph?

LangGraph helps organize agent workflows as nodes and edges.

A node is one step:

```text
retrieve evidence
```

An edge says what happens next:

```text
after retrieve evidence, check the claim
```

This makes the workflow easier to inspect, extend, and debug.

## What Is State?

LangGraph nodes share a state object.

For our project, state contains things like:

```text
claim
subclaims
subclaim_results
aggregation
report
```

Each node reads part of the state and returns updates.

## What Changes?

The core behavior does not change yet.

We are changing the orchestration style:

```text
Before: one Python function calls another Python function
Now: LangGraph runs named workflow nodes in order
```

## Why This Matters Later

Later, LangGraph can help with:

1. Branching
2. Retries
3. Human review steps
4. More complex agent workflows
5. Clear architecture diagrams

## Key Takeaway

LangGraph is not replacing our fact-checking logic.

It is organizing the logic into a graph-shaped workflow.
