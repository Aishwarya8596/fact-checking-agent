# Session 1: Foundations

## What We Are Building

Our larger project is a Fact Checking Agentic System.

Given a claim like:

> The Eiffel Tower is in Berlin.

the system should eventually:

1. Understand the claim.
2. Search for or receive evidence.
3. Decide whether the evidence supports, contradicts, or is not enough to verify the claim.
4. Explain the judgment using only the evidence.
5. Return the answer in a structured format we can test.

But before building that, we need to understand why a normal LLM answer is not enough.

## Mini Lesson: What Stochastic Means

Stochastic means involving randomness or probability.

An LLM does not usually choose the single "correct" next word in a rigid way. It estimates many possible next tokens and samples from them. That is why the same prompt can sometimes produce different answers.

Example prompt:

```text
Tell me one reason fact checking is hard.
```

Possible answers:

```text
Sources can disagree.
```

```text
Claims may depend on fresh information.
```

```text
The wording of a claim can be ambiguous.
```

All three can be reasonable. The model is not necessarily broken because it varies. The problem is that this same flexibility can also produce unsupported, vague, or overconfident answers.

## Tiny Demo: Same Prompt, Different Answers

Run:

```bash
python3 demos/session_01_stochastic_prompting.py
```

The script simulates a model choosing from several plausible answers. It is not a real LLM, but it demonstrates the core idea: generation can involve sampling.

## Why Prompts Fail

A weak prompt often leaves too much unspecified.

Weak prompt:

```text
Is this claim true? The Eiffel Tower is in Berlin.
```

Possible problem:

```text
No, that sounds false.
```

This answer is probably right, but it is not good enough for a fact-checking system. Why?

1. It gives no evidence.
2. It does not say what standard it used.
3. It might rely on memory instead of sources.
4. It is hard to evaluate automatically.

Better prompt:

```text
Use only the evidence below.
Classify the claim as supported, contradicted, or not enough evidence.
Return a short explanation.

Claim: The Eiffel Tower is in Berlin.
Evidence: The Eiffel Tower is a landmark in Paris, France.
```

Better answer:

```text
Contradicted. The evidence says the Eiffel Tower is in Paris, France, not Berlin.
```

## Why Structure Helps

Plain English is easy for humans, but hard for software to check.

Instead of asking for:

```text
Tell me if the claim is true.
```

we can ask for JSON:

```json
{
  "verdict": "contradicted",
  "confidence": 0.94,
  "explanation": "The evidence places the Eiffel Tower in Paris, France, not Berlin."
}
```

This is useful because later our code can check:

1. Is `verdict` one of the allowed labels?
2. Is `confidence` a number between 0 and 1?
3. Does the explanation cite the evidence?

## Evaluation: How Do We Know It Is Good?

For a fact-checking system, a single good-looking answer is not enough.

We need test examples:

```json
{
  "claim": "The Eiffel Tower is in Berlin.",
  "evidence": "The Eiffel Tower is a landmark in Paris, France.",
  "expected_verdict": "contradicted"
}
```

Then we compare the system output against the expected answer.

This gives us a basic evaluation loop:

1. Run the system on examples.
2. Compare outputs to expected verdicts.
3. Inspect mistakes.
4. Improve prompts, evidence retrieval, or output structure.
5. Run the examples again.

## Key Takeaways

1. LLMs are flexible because they generate probabilistically.
2. Flexibility is useful, but it can create inconsistency.
3. Prompts reduce ambiguity, but prompts alone are not enough.
4. Structured output makes answers easier to validate.
5. Evaluation tells us whether changes actually improve the system.

## Next Session

In Session 2, we will create our first tiny fact-checking pipeline:

1. Input a claim.
2. Provide evidence manually.
3. Ask for a structured verdict.
4. Validate the output.
5. Add a few evaluation examples.
