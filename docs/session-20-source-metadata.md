# Session 20: Source Metadata

## What We Are Building

In earlier sessions, evidence looked like this:

```json
{
  "id": "evidence_1",
  "text": "The Eiffel Tower is a landmark in Paris, France."
}
```

In Session 20, evidence includes source metadata:

```json
{
  "id": "evidence_1",
  "title": "Eiffel Tower Location Note",
  "source_type": "local_demo_fact",
  "url": "local://eiffel-tower-location",
  "text": "The Eiffel Tower is a landmark in Paris, France."
}
```

## Why This Matters

A real fact-checking system should not only say:

```text
I used evidence_1.
```

It should also show where that evidence came from:

```text
title
source type
URL
```

For now, these are local demo sources, not real web pages.

Later, when we add web retrieval, these same fields can hold real source titles and URLs.

## Key Takeaway

Citation IDs identify evidence inside our system.

Source metadata explains where that evidence came from.
