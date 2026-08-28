# Session 11: Evaluate The Retrieval Pipeline

## What We Are Building

In Session 10, we added retrieval:

```text
claim -> retrieve evidence -> model verdict
```

In Session 11, we evaluate that full pipeline.

## Why This Matters

Once retrieval is added, there are two major places the system can fail:

1. Retrieval fails to find useful evidence.
2. The model gets useful evidence but chooses the wrong verdict.

These are different bugs.

If retrieval gives the model bad evidence, the model may fail even with a good prompt.

If retrieval gives the model good evidence and the model still fails, then the prompt or reasoning step may need improvement.

## Metrics In This Session

We measure two things.

### Retrieval Hit Rate

Retrieval hit rate asks:

```text
Did the retriever return at least one evidence item we expected?
```

Example:

```text
Expected useful evidence: evidence_1
Retrieved evidence: evidence_1, evidence_2
```

That is a hit.

### Verdict Accuracy

Verdict accuracy asks:

```text
Did the final model verdict match the expected verdict?
```

This is the same basic accuracy idea from earlier sessions.

## Why Separate These Metrics?

Imagine the final verdict is wrong.

Without separate metrics, we only know:

```text
The system failed.
```

With separate metrics, we can ask:

```text
Did retrieval fail?
Did the model reasoning fail?
Did both fail?
```

That makes debugging easier.

## Key Takeaway

RAG systems need evaluation at multiple steps.

For our fact-checking agent, we now care about:

1. Did we retrieve useful evidence?
2. Did the model return valid output?
3. Did the model cite real evidence IDs?
4. Did the model choose the right verdict?
