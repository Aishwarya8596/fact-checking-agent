# Session 10: Local Retrieval

## What We Are Building

Until now, we manually chose the evidence items.

In Session 10, we add a tiny retrieval step:

```text
claim -> local evidence store -> relevant evidence -> fact-checking model
```

This is the first small version of Retrieval-Augmented Generation, often called RAG.

## What Retrieval Means

Retrieval means:

```text
Find useful information before asking the model to answer.
```

For fact checking, this matters because the model should not rely only on memory.

Instead, we want this pattern:

```text
Claim comes in.
System finds evidence.
Model uses only that evidence.
Model returns verdict and citations.
```

## Why Local Retrieval First?

We are not using web search yet.

A web search step adds extra complexity:

1. Search API setup
2. Network calls
3. Source quality
4. Parsing web pages
5. Handling noisy results

So first we use a tiny local evidence store. That lets us learn the retrieval idea without the web.

## How The Simple Retriever Works

The retriever:

1. Takes meaningful words from the claim.
2. Takes meaningful words from each evidence item.
3. Counts how many words overlap.
4. Returns the highest scoring evidence items.

Example:

```text
Claim: The Eiffel Tower is in Berlin.
Evidence: The Eiffel Tower is a landmark in Paris, France.
```

Shared meaningful words:

```text
eiffel, tower
```

So this evidence is likely relevant.

## This Is Not Perfect

This is a beginner retrieval method.

Later, stronger retrieval can use:

1. Embeddings
2. Vector databases
3. Search APIs
4. Reranking
5. Source credibility filters

## Key Takeaway

We are adding another system step:

```text
before reasoning, retrieve evidence
```

This is a major idea behind reliable LLM applications.
