# Session 14: Final Verdict Aggregation

## What We Are Building

In Session 13, the system checked each subclaim separately.

In Session 14, we add a final aggregation step:

```text
subclaim verdicts -> overall verdict
```

## Why Aggregation Matters

A complex claim can contain multiple smaller claims.

Example:

```text
The Eiffel Tower is in Paris and Mars is known as the Red Planet.
```

If both subclaims are supported, the whole claim is supported.

But if one part is supported and one part is contradicted, the whole claim should not be simply marked supported.

## Verdict Rules

For now, we use simple transparent rules:

```text
If any subclaim is contradicted:
    final verdict = partially_supported

Else if any subclaim has not enough evidence:
    final verdict = uncertain

Else if all subclaims are supported:
    final verdict = supported
```

We use `partially_supported` when at least one part works and at least one part fails.

## Why Rule-Based Aggregation?

We could ask another LLM to combine the results.

But for this beginner version, rules are better because they are:

1. Easy to read
2. Easy to test
3. Predictable
4. Not dependent on another model call

## Key Takeaway

The model checks individual subclaims.

Code combines the results into a final verdict.

This is a useful pattern:

```text
LLM for language reasoning
code for deterministic control logic
```
