# Session 24: Wikipedia Retrieval

## What We Are Building

In Session 24, we add our first real web retrieval demo.

Instead of using only local evidence, we search Wikipedia:

```text
claim -> Wikipedia search -> evidence items with real URLs
```

## Why Wikipedia First?

Wikipedia is not perfect, but it is useful for a beginner web retrieval step because:

1. It has a public API.
2. It returns structured data.
3. It does not require an API key.
4. It gives real page URLs.

This is still not the final fact-checking retrieval system. It is a controlled first step.

## What The Retriever Returns

The retriever converts Wikipedia search results into our evidence shape:

```json
{
  "id": "web_evidence_1",
  "title": "2022 FIFA World Cup final",
  "source_type": "encyclopedia",
  "source_quality": "medium",
  "source_score": 0.8,
  "url": "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_final",
  "text": "Short snippet from the search result."
}
```

## Why This Is Not Full Web Search Yet

This version searches Wikipedia only.

It does not search:

1. Government websites
2. News websites
3. Academic sources
4. Official sports websites
5. Social media

That is okay. We are learning one step at a time.

## Key Takeaway

The system is starting to retrieve evidence from outside our codebase.

But we still keep the safety pattern:

```text
retrieve evidence first
then ask the model to reason only from that evidence
```
