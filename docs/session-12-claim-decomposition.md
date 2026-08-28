# Session 12: Claim Decomposition

## What We Are Building

So far, we fact-checked one claim at a time.

In Session 12, we add claim decomposition:

```text
complex claim -> smaller checkable subclaims
```

## Why Decomposition Matters

Some claims contain more than one fact.

Example:

```text
The Eiffel Tower is in Paris and Berlin is the capital of Germany.
```

This contains two checkable parts:

```text
1. The Eiffel Tower is in Paris.
2. Berlin is the capital of Germany.
```

If we only return one verdict for the whole sentence, we may lose important detail.

## Why This Is Agentic

Agentic systems often break a task into smaller steps before solving it.

For fact checking, a useful workflow is:

```text
claim -> decompose -> retrieve evidence for each subclaim -> verify each subclaim -> combine results
```

This is more controlled than asking:

```text
Is this whole claim true?
```

## What The Model Returns

The model returns structured JSON:

```json
{
  "original_claim": "...",
  "subclaims": [
    {
      "id": "subclaim_1",
      "text": "..."
    }
  ]
}
```

Each subclaim should be:

1. Small
2. Clear
3. Checkable using evidence
4. Not a question

## Key Takeaway

Claim decomposition helps us turn a messy real-world claim into smaller pieces our system can retrieve evidence for and evaluate.
