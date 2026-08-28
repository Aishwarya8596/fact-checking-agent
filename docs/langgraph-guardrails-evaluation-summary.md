# LangGraph, Guardrails, And Evaluation Summary

## 1. LangGraph Nodes / DAG

Our current LangGraph workflow is mostly linear, with one guardrail branch at the start:

```text
START
-> validate_input
   -> if valid: decompose_claim
      -> check_subclaims
      -> aggregate_verdict
      -> build_report
   -> if invalid: build_guardrail_report
-> END
```

The nodes are:

### validate_input

Checks whether the user entered a factual claim.

If the input looks like a question, the system stops early and asks the user to rewrite it as a claim.

### decompose_claim

Breaks the original claim into smaller subclaims.

### check_subclaims

Retrieves evidence for each subclaim, uses local evidence first, falls back to Wikipedia if needed, asks OpenAI to fact-check, and validates citation IDs.

### aggregate_verdict

Combines all subclaim verdicts into one final verdict.

### build_report

Creates the final structured report shown in Gradio.

## 2. Current Guardrails

We currently have beginner-level guardrails:

```text
evidence-grounding instructions
structured JSON schema
citation ID validation
question/input guardrail
retrieval fallback
rule-based verdict aggregation
source metadata and source quality
evaluation script
```

These help reduce hallucination and make the model output easier to inspect and test.

## 3. Missing Production-Grade Guardrails

We do not yet have full production guardrails such as:

```text
prompt injection defense
strong hallucination detection
entity/date-aware retrieval
human review
advanced source credibility checking
confidence calibration
```

These can be added later as the project becomes more advanced.

## 4. Evaluation Criteria

Our current main evaluation metric is:

```text
final verdict accuracy
```

We also track:

```text
citation validation rate
retrieval source usage
```

Evaluation is mainly for developers, not end users.

```text
User mode:
one claim -> one answer

Developer/evaluation mode:
many claims -> measure reliability
```

## 5. Agents / Components

We implemented one main Fact-Checking Agent as a LangGraph workflow.

Internally, it has agent-like components:

```text
Claim Decomposer
Evidence Retriever
Evidence-Based Verifier
Citation Validator
Verdict Aggregator
Report Generator
```

Technically, these are LangGraph nodes/components, not separate autonomous agents.

## 6. Local Retrieval Weakness

We tested:

```text
California's capital is Sacramento.
```

The system returned `uncertain` because local retrieval matched weak evidence:

```text
Berlin is the capital city of Germany.
```

It matched only the word:

```text
capital
```

So the system used local evidence and did not fall back to Wikipedia.

We fixed this by requiring stronger local relevance:

```text
min_relevance_score = 2
```

So one generic word match no longer blocks Wikipedia fallback.

## 7. Better Future Retrieval

We also discussed a harder case:

```text
Argentina won the FIFA 2026 World Cup.
```

This might retrieve:

```text
Argentina won the 2022 FIFA World Cup.
```

because many words overlap.

The better future fix is:

```text
entity/date-aware retrieval
conflict-aware evidence selection
```

The important lesson:

```text
Fact-checking retrieval should find both supporting and contradicting evidence.
```

So the next retrieval improvement later should detect:

```text
same entity/topic
different date/year
possible contradiction
```

## 8. Retrieval Test Claims

These are useful claims to test in Gradio after retrieval changes.

### No Local Evidence, Should Use Wikipedia

```text
California's capital is Sacramento.
```

Expected behavior:

```text
verdict: supported
retrieval source: wikipedia
```

Why this matters:

```text
The local evidence store does not contain California/Sacramento evidence.
The system should avoid using weak local evidence such as "Berlin is the capital city of Germany."
```

### Same Topic, Wrong Year

```text
Argentina won the FIFA 2026 World Cup.
```

Expected behavior:

```text
verdict: contradicted or uncertain depending on retrieved Wikipedia evidence
retrieval source: local+wikipedia or wikipedia
```

Why this matters:

```text
Local evidence says Argentina won the 2022 FIFA World Cup.
The claim says 2026, so retrieval should notice the year conflict instead of treating 2022 evidence as enough.
```

### Same Event, Wrong Winner

```text
The USA won the FIFA 2022 World Cup.
```

Expected behavior:

```text
verdict: contradicted
retrieval source: local
```

Why this matters:

```text
The local evidence store says Argentina won the 2022 FIFA World Cup.
That evidence directly contradicts the USA claim.
```

### Related Words, Not Enough Evidence

```text
Coffee was first discovered in Brazil.
```

Expected behavior:

```text
verdict: uncertain
```

Why this matters:

```text
Local evidence says coffee is grown in Brazil today.
That does not prove coffee was first discovered in Brazil.
```

### Subjective Claim

```text
Apple is the best company in the world.
```

Expected behavior:

```text
verdict: uncertain
```

Why this matters:

```text
"Best" is subjective unless we define a measurable standard.
The fact-checker should avoid pretending opinion claims are factual.
```

### Question Instead Of Claim

```text
Who won the FIFA 2026 World Cup?
```

Expected behavior:

```text
verdict: input_required
message: ask the user to rewrite the question as a factual claim
```

Example rewrite:

```text
"Spain won the FIFA 2026 World Cup."
```

Why this matters:

```text
Our system is designed to verify claims, not answer open questions.
```

Known limitation to revisit later:

```text
The current guardrail treats any input ending with "?" as a question.
That means a claim-like input such as "California's capital is Sacramento?"
also returns input_required.
```

Why this is acceptable for now:

```text
The app asks users to enter factual claims.
The clean input should be written as: "California's capital is Sacramento."
```

Possible future improvement:

```text
Add a smarter input classifier that separates:
1. real questions
2. claim-like statements with question punctuation
3. subjective/opinion statements
```

### Mixed Multi-Part Claim

```text
Sacramento is the capital of California and the USA won the FIFA 2026 World Cup.
```

Expected behavior:

```text
verdict: partially_supported, contradicted, or uncertain depending on the subclaim verdicts
```

Why this matters:

```text
The first subclaim can be supported.
The second subclaim may be contradicted or uncertain depending on retrieved evidence.
This tests decomposition plus final verdict aggregation.
```

When testing retrieval, inspect:

```text
final verdict
retrieval source
retrieved evidence
citation_ids
retrieval diagnostics
final reason
```
