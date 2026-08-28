# Session 7: Groundedness

## What We Are Building

So far, we have checked:

1. Verdict accuracy
2. Output validation

Now we add a new question:

```text
Is the explanation grounded in the evidence?
```

Grounded means the answer is based on the provided evidence, not outside memory or unsupported details.

## Why Groundedness Matters

For a fact-checking system, a model should not say:

```text
The Eiffel Tower is in Paris because it was built for the 1889 World's Fair.
```

if the evidence only says:

```text
The Eiffel Tower is a landmark in Paris, France.
```

The extra detail may be true, but it did not come from the provided evidence.

Our system should reward answers that stay close to evidence.

## A Simple First Heuristic

In this session, we use a simple check:

```text
How many meaningful explanation words also appear in the evidence?
```

Example:

```text
Evidence: The Eiffel Tower is a landmark in Paris, France.
Explanation: The evidence says the Eiffel Tower is in Paris, not Berlin.
```

Shared meaningful words:

```text
eiffel, tower, paris
```

That suggests the explanation is at least connected to the evidence.

## This Is Not Perfect

This check is only a beginner heuristic.

It can miss good explanations that use synonyms. It can also pass explanations that copy evidence words but still reason badly.

Later, stronger groundedness checks can use:

1. Citation matching
2. Sentence-level evidence references
3. LLM-as-judge evaluation
4. Human review samples
5. Retrieval source comparison

## Key Takeaway

Accuracy checks the verdict.

Validation checks the shape.

Groundedness checks whether the explanation is connected to the evidence.

Reliable AI systems usually need all three.
