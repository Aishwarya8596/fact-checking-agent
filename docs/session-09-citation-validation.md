# Session 9: Citation Validation

## What We Are Building

In Session 8, we asked the model to return citation IDs:

```json
{
  "citation_ids": ["evidence_1"]
}
```

In Session 9, we check whether those citation IDs are valid.

## Why Citation Validation Matters

The model is instructed to choose only from the evidence IDs we provide.

But in real systems, we still verify important assumptions in code.

For example, if we provide:

```text
evidence_1
evidence_2
```

then this is valid:

```json
{
  "citation_ids": ["evidence_1"]
}
```

But this is invalid:

```json
{
  "citation_ids": ["evidence_99"]
}
```

`evidence_99` was never provided, so our system should catch it.

## What We Validate

We check:

1. `citation_ids` exists.
2. `citation_ids` is a list.
3. Every citation ID is a string.
4. Every citation ID appears in the provided evidence items.

## Why This Is An Agentic System Habit

Agentic systems often have several steps:

```text
retrieve evidence -> reason over evidence -> write final answer
```

Each step should check that the previous step returned usable data.

Citation validation protects the final answer from citing sources that do not exist.

## Key Takeaway

Prompt instructions are helpful, but code validation is stronger.

We tell the model what to do, then we verify that it actually did it.
