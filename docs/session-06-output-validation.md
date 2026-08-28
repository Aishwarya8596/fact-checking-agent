# Session 6: Output Validation

## What We Are Building

In Session 5, we measured verdict accuracy:

```text
actual verdict == expected verdict
```

In Session 6, we add output validation:

```text
model output -> check required fields and values -> valid or invalid
```

## Why Validation Is Different From Accuracy

Accuracy asks:

```text
Did the model choose the correct verdict?
```

Validation asks:

```text
Can our program safely use this output?
```

These are different.

For example, this could be accurate but not valid:

```json
{
  "answer": "contradicted"
}
```

The verdict is present in human language, but our program expected a field named `verdict`.

## What We Validate

For now, we check:

1. The output is a dictionary.
2. All required fields exist.
3. The verdict is one of the allowed labels.
4. Confidence is a number between 0 and 1.
5. Claim, evidence, and explanation are non-empty strings.

## Why This Matters For Agents

Agentic systems often pass one step's output into the next step.

If one step returns a broken shape, later steps can fail or behave strangely.

For our fact-checking agent, future steps may need:

1. The verdict for evaluation.
2. The explanation for the user interface.
3. The confidence for ranking or warnings.
4. The evidence for citations.

Validation protects those later steps.

## Key Takeaway

A good AI system checks both:

```text
Is the answer correct?
Is the answer usable by software?
```

Accuracy helps with correctness. Validation helps with reliability.
