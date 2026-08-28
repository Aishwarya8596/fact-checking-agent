# Session 31: Number Conflict Wikipedia Fallback

## What Problem We Found

These claims returned `uncertain`:

```text
The USA won the FIFA 2026 World Cup.
Argentina won the FIFA 2026 World Cup.
```

The system found local evidence about:

```text
Argentina won the 2022 FIFA World Cup.
```

That local evidence was related, but not enough to answer a 2026 claim.

## Why It Happened

Session 30 detected the number conflict:

```text
claim number: 2026
evidence number: 2022
```

But the graph still only passed local evidence to the model.

The model correctly returned `uncertain` because 2022 evidence alone does not prove who won in 2026.

## Fix

If local evidence has a number conflict, the graph now also retrieves Wikipedia evidence:

```text
local evidence has number conflict
-> supplement with Wikipedia evidence
-> model receives both local and web evidence
```

The retrieval source can now be:

```text
local+wikipedia
```

## Key Takeaway

Detecting a conflict is useful, but not always enough.

When the system detects an important date or number mismatch, it should retrieve more evidence before asking the model for a verdict.
