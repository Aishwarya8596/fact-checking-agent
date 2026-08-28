# Session 25: Wikipedia Retrieval Fallback

## What We Are Building

In Session 25, we connect Wikipedia retrieval to the LangGraph workflow.

The new retrieval behavior is:

```text
try local retrieval first
if local retrieval finds nothing, use Wikipedia retrieval
```

## Why Use A Fallback?

Our local evidence store is small.

If it has useful evidence, we use it because it is fast and predictable.

If it has nothing useful, we ask Wikipedia for external evidence.

## Updated Workflow

```text
subclaim
-> local retrieval
-> if no evidence, Wikipedia retrieval
-> OpenAI fact-checking with citations
-> citation validation
```

## Why Not Always Use Wikipedia?

For this beginner project, local evidence is still useful because:

1. It is predictable.
2. It is fast.
3. It helps us test simple examples.
4. It avoids unnecessary network calls.

Wikipedia is now the backup for claims not covered locally.

## Key Takeaway

The system is becoming more realistic:

```text
retrieve from known local evidence first
fall back to external evidence when needed
```
