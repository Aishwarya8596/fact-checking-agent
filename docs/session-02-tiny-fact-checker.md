# Session 2: Tiny Fact Checker

## What We Are Building

In Session 1, we saw what a good structured answer could look like.

In Session 2, we make the first tiny version of the system:

```text
claim + evidence -> verdict JSON
```

This is not using an LLM yet. It uses simple rules so we can focus on the system design.

## Why No LLM Yet?

If we add the LLM too early, many things become mixed together:

1. Did the prompt fail?
2. Did the model misunderstand the evidence?
3. Did the JSON format break?
4. Did the evaluation logic fail?
5. Did the API call fail?

That is too much at once for a beginner-friendly project.

So first we build a small predictable version. Then we replace the simple rules with an LLM call later.

## The Core Idea

A fact-checking system should not simply ask:

```text
Is this claim true?
```

Instead, it should ask:

```text
Given this claim and this evidence, what verdict is supported by the evidence?
```

That distinction matters.

The system is not judging truth from memory. It is judging whether the provided evidence supports or contradicts the claim.

## Verdict Labels

For now, we use three labels:

```text
supported
contradicted
not_enough_evidence
```

Later we can add:

```text
partially_supported
```

But starting with three labels keeps the first version easier to understand and test.

## What To Notice

Run:

```bash
python3 demos/session_02_tiny_fact_checker.py
```

Notice that every output has the same JSON shape:

```json
{
  "claim": "...",
  "evidence": "...",
  "verdict": "...",
  "confidence": 0.0,
  "explanation": "..."
}
```

That consistent shape is important because later we can build evaluation around it.

## Key Takeaway

We are separating the project into small layers:

1. Define the input and output shape.
2. Make the output structured.
3. Evaluate whether the verdict is correct.
4. Replace simple rules with an LLM.
5. Add retrieval so the system can find evidence itself.
