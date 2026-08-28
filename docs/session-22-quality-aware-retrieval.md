# Session 22: Quality-Aware Retrieval

## What We Are Building

In Session 21, we added source quality metadata.

In Session 22, retrieval starts using that metadata.

## Previous Retrieval Score

Before, retrieval used only word overlap:

```text
score = number of shared meaningful words
```

That means evidence with more matching words ranked higher.

## New Retrieval Score

Now retrieval uses:

```text
combined_score = relevance_score + source_score * 0.1
```

Where:

```text
relevance_score = shared meaningful words
source_score = quality score from the evidence item
```

## Why Source Quality Is A Small Weight

Relevance should still matter most.

A high-quality source that is unrelated to the claim should not beat a relevant source.

So source quality only gives a small boost.

## Example

If two evidence items both match the claim equally well, the one with a stronger `source_score` can rank higher.

## Key Takeaway

Good retrieval needs both:

```text
Is this evidence relevant?
Is this evidence reliable?
```

This is our first small step toward combining those ideas.
