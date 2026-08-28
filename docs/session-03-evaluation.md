# Session 3: Evaluation

## What We Are Building

In Session 2, we created a tiny fact checker:

```text
claim + evidence -> structured verdict
```

In Session 3, we add evaluation:

```text
examples with expected answers -> run system -> measure correctness
```

## Why Evaluation Matters

When working with LLMs, a response can sound good but still be wrong.

For a fact-checking system, we need a way to ask:

```text
Did the system return the verdict we expected?
```

That is evaluation.

## Test Examples

Each test example has:

1. A claim
2. Evidence
3. The expected verdict

Example:

```json
{
  "claim": "The Eiffel Tower is in Berlin.",
  "evidence": "The Eiffel Tower is a landmark in Paris, France.",
  "expected_verdict": "contradicted"
}
```

The system returns a verdict. The evaluator compares:

```text
actual verdict vs expected verdict
```

## Accuracy

Accuracy means:

```text
number correct / total number of examples
```

If we test 3 examples and the system gets 2 correct:

```text
accuracy = 2 / 3 = 66.7%
```

Accuracy is not the only metric used in real AI systems, but it is the easiest place to start.

## Why This Helps Later

When we add an LLM, we will change prompts often.

Without evaluation, we might say:

```text
This prompt feels better.
```

With evaluation, we can say:

```text
This prompt improved accuracy from 60% to 80% on our examples.
```

That is a much stronger engineering habit.

## Key Takeaway

Evaluation gives us a feedback loop:

1. Build a version.
2. Run examples.
3. Measure results.
4. Inspect failures.
5. Improve the system.
6. Run the examples again.
