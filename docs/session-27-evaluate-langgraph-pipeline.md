# Session 27: Evaluate LangGraph Pipeline

## What We Are Building

In this session, we add an evaluation script for the current full pipeline:

```text
claim -> LangGraph workflow -> final report -> evaluation
```

## Why This Matters

The Gradio app is useful for manual testing.

But manual testing is not enough.

We need repeatable checks that tell us:

1. Did the final verdict match what we expected?
2. Did citation validation pass?
3. Did retrieval come from local evidence or Wikipedia?

## What We Measure

### Final Verdict Accuracy

```text
actual final verdict == expected final verdict
```

### Citation Validation Rate

```text
subclaims with valid citations / total subclaims
```

### Retrieval Source Usage

We print whether each subclaim used:

```text
local
wikipedia
```

## Why This Helps

If a future change breaks the system, this script can catch it.

For example, this kind of evaluation would have helped us notice the earlier aggregation bug:

```text
single contradicted claim -> should be contradicted, not partially_supported
```

## Key Takeaway

A working demo is good.

A repeatable evaluation is better.
