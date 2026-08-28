# Session 5: Evaluate OpenAI Output

## What We Are Building

In Session 4, we asked the OpenAI model to return one structured fact-checking result.

In Session 5, we run multiple examples:

```text
test examples -> OpenAI fact checker -> compare verdicts -> accuracy
```

## Why This Matters

An LLM answer can look polished even when it is wrong.

Evaluation helps us avoid judging only by appearance.

Instead of asking:

```text
Does this response sound good?
```

we ask:

```text
Did the model choose the expected verdict?
```

## What We Are Measuring

For now, we still measure verdict accuracy:

```text
correct verdicts / total examples
```

This is simple, but it gives us a useful starting point.

Later, we will add more checks:

1. Did the model return valid JSON?
2. Did it use only the evidence?
3. Did the explanation match the verdict?
4. Did it cite the right source?
5. Did it admit uncertainty when evidence was weak?

## Why Use The Same Examples?

We use the same examples from the rule-based evaluator so the comparison is easy:

```text
same inputs
same expected verdicts
different fact-checking engine
```

The engine changed from rules to an LLM, but our evaluation idea stayed the same.

## Key Takeaway

This is the core project loop:

```text
change the system -> run evaluation -> inspect mistakes -> improve
```

That loop is more important than any single prompt.
