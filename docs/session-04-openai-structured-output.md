# Session 4: OpenAI Structured Output

## What We Are Building

In Session 2, the verdict was produced by simple hardcoded rules.

In Session 4, the verdict is produced by an LLM:

```text
claim + evidence -> OpenAI API -> structured verdict JSON
```

The output shape stays the same:

```json
{
  "claim": "...",
  "evidence": "...",
  "verdict": "supported | contradicted | not_enough_evidence",
  "confidence": 0.0,
  "explanation": "..."
}
```

## Why This Step Matters

This is the first time the project uses a real language model.

But we are still keeping the task small:

1. No web search yet.
2. No Gradio UI yet.
3. No LangSmith tracing yet.
4. No automatic claim decomposition yet.

The LLM only has one job:

```text
Given a claim and evidence, classify the verdict using only the evidence.
```

## Why Structured Output Matters

If we ask for a normal paragraph, the model might return many different formats.

Example:

```text
The claim is false because the Eiffel Tower is in Paris.
```

That is readable, but harder for code to evaluate.

Structured JSON is better for engineering:

```json
{
  "verdict": "contradicted",
  "confidence": 0.95,
  "explanation": "The evidence says the Eiffel Tower is in Paris, France, not Berlin."
}
```

Now our code can check:

1. Is the verdict an allowed label?
2. Is confidence a number?
3. Is the explanation present?
4. Did the verdict match the expected answer?

## What The Prompt Tells The Model

The prompt says:

1. Use only the provided evidence.
2. Do not rely on memory.
3. Choose one allowed verdict.
4. Return JSON matching our schema.

This is the beginning of reliability work.

## Key Takeaway

We are replacing the rule-based brain with an LLM, but keeping the same interface:

```text
input shape stays the same
output shape stays the same
implementation changes inside
```

That is a strong design habit. It lets us improve one part of the system without rewriting everything else.
