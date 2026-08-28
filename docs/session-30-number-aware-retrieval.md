# Session 30: Number-Aware Retrieval

## What Problem We Are Solving

Word overlap alone is not enough for fact checking.

Example:

```text
Claim: Argentina won the FIFA 2026 World Cup.
Evidence: Argentina won the 2022 FIFA World Cup.
```

These texts share many words:

```text
Argentina, won, FIFA, World, Cup
```

But the year is different:

```text
claim year: 2026
evidence year: 2022
```

That difference matters.

## What We Added

The retriever now extracts numbers from the claim and evidence.

It tracks:

```text
claim_numbers
evidence_numbers
shared_numbers
conflicting_numbers
number_conflict
```

## Why This Helps

For fact checking, contradictory evidence is useful.

If evidence is about the same topic but has a different date or number, we should often still retrieve it so the model can decide whether it contradicts the claim.

## Important Idea

Retrieval should not only find evidence that supports a claim.

It should also find evidence that may contradict the claim.

## What The UI Shows

The readable report now includes retrieval diagnostics, such as:

```text
shared_words
claim_numbers
evidence_numbers
number_conflict
```

This helps us debug why evidence was selected.
