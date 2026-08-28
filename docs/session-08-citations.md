# Session 8: Citations

## What We Are Building

Until now, our examples had one evidence string:

```text
Claim + Evidence -> Verdict
```

In real fact checking, we often have multiple evidence snippets:

```text
Claim + Evidence 1 + Evidence 2 + Evidence 3 -> Verdict with citations
```

So in Session 8, we add citation IDs.

## Why Citations Matter

If the system says:

```text
The claim is contradicted.
```

we should be able to ask:

```text
Which evidence caused that verdict?
```

Without citations, the answer is harder to inspect.

With citations, the model can return:

```json
{
  "verdict": "contradicted",
  "citation_ids": ["evidence_1"]
}
```

That means:

```text
The model used evidence_1 to justify the verdict.
```

## What Changes In The Output

Earlier output:

```json
{
  "claim": "...",
  "evidence": "...",
  "verdict": "contradicted",
  "confidence": 0.95,
  "explanation": "..."
}
```

New output:

```json
{
  "claim": "...",
  "verdict": "contradicted",
  "confidence": 0.95,
  "explanation": "...",
  "citation_ids": ["evidence_1"]
}
```

We removed the single `evidence` field because now there can be many evidence items.

## Why This Helps Later

When we add retrieval, the system will search for sources.

Each source can become an evidence item:

```text
evidence_1: official report
evidence_2: trusted news article
evidence_3: encyclopedia page
```

Then the final answer can cite the exact evidence it used.

## Key Takeaway

Citations make the fact-checker more inspectable.

The goal is not only:

```text
Give an answer.
```

The goal is:

```text
Give an answer and show which evidence supports it.
```
