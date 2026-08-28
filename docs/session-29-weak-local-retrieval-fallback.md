# Session 29: Weak Local Retrieval Fallback

## What Problem We Found

The claim:

```text
California's capital is Sacramento.
```

was returning `uncertain`.

The system retrieved local Berlin evidence because both texts contained the word:

```text
capital
```

That weak match blocked Wikipedia fallback.

## Why It Happened

Our local retriever treated any word overlap as enough.

So this matched:

```text
Claim: California's capital is Sacramento.
Evidence: Berlin is the capital city of Germany.
Shared word: capital
```

But this evidence is not actually useful for the claim.

## Fix

We added a minimum relevance threshold for local retrieval inside the graph:

```text
min_relevance_score = 2
```

That means local evidence needs at least two meaningful word overlaps before it blocks Wikipedia fallback.

## Key Takeaway

Retrieval should not only ask:

```text
Did anything match?
```

It should ask:

```text
Did enough relevant evidence match?
```
