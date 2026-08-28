# Session 21: Source Quality

## What We Are Building

In Session 20, we added source metadata:

```text
title
source_type
url
```

In Session 21, we add source quality metadata:

```text
source_quality
source_score
```

## Why Source Quality Matters

Not all evidence should be treated equally.

For example:

```text
official report > trusted encyclopedia > random blog > social media post
```

Our current evidence is still local demo evidence, but we can start modeling this idea now.

## New Fields

`source_quality` is a human-readable label:

```text
demo_verified
demo_partial
unknown
```

`source_score` is a simple number:

```text
0.8 = stronger demo source
0.5 = weaker or incomplete demo source
```

## Why This Helps Later

When we add web retrieval, source quality can help us:

1. Prefer official or trusted sources.
2. Warn when evidence is weak.
3. Avoid overconfident verdicts from poor evidence.
4. Explain why a source was used.

## Key Takeaway

Fact checking is not only about finding evidence.

It is also about judging whether the evidence is reliable enough to use.
