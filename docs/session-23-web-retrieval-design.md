# Session 23: Web Retrieval Design

## What We Are Designing

So far, our evidence comes from a small local list inside the code.

Current flow:

```text
claim -> local evidence store -> retrieved evidence -> model verdict
```

Next flow:

```text
claim -> web search -> web evidence -> model verdict
```

Before writing code, we define what good web retrieval should do.

## Why We Need Web Retrieval

The local evidence store only knows facts we manually added.

That is why a claim like:

```text
Argentina won the FIFA 2022 World Cup.
```

only worked after we added a local evidence item.

With web retrieval, the system can look for evidence outside the local demo list.

## Important Rule

The model still should not guess from memory.

Even with web retrieval, the safe pattern is:

```text
retrieve evidence first
then ask the model to judge using only that evidence
```

## Web Evidence Shape

Every web evidence item should use the same shape as our local evidence:

```json
{
  "id": "evidence_1",
  "title": "Page title",
  "source_type": "official | encyclopedia | news | blog | unknown",
  "source_quality": "high | medium | low | unknown",
  "source_score": 0.9,
  "url": "https://example.com/source-page",
  "text": "Short evidence snippet from the page."
}
```

This keeps the rest of our pipeline stable.

## Source Quality Rules

For a beginner version, we can use simple rules:

```text
official source -> high quality -> 0.9
trusted encyclopedia -> high/medium quality -> 0.8
established news source -> medium quality -> 0.7
blog/forum/social post -> low quality -> 0.4
unknown source -> unknown quality -> 0.3
```

These rules are not perfect. They are a starting point.

## Retrieval Rules

For the first web version:

1. Search the web for the claim.
2. Keep the top few results.
3. Store title, URL, snippet, source type, and quality score.
4. Give those snippets to the model.
5. Ask the model to choose citations only from those evidence IDs.

## What Can Go Wrong?

Web retrieval adds new failure modes:

1. Search results may be irrelevant.
2. Snippets may be too short.
3. Sources may be low quality.
4. Pages may disagree.
5. Search may return outdated information.
6. A real page may require JavaScript or be hard to parse.

## How We Handle Uncertainty

If web evidence is weak or conflicting, the model should return:

```text
not_enough_evidence
```

It should not force a confident answer.

## First Implementation Choice

For Session 24, we can start with a simple search API or search helper that returns:

```text
title
url
snippet
```

Then we convert those search results into our evidence format.

## Key Takeaway

Web retrieval does not mean:

```text
Let the model browse and answer freely.
```

It means:

```text
Search for evidence, structure it, score it, then ask the model to reason only from that evidence.
```
