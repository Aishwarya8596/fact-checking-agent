# Fact Checking Agentic System: PPT Talk Track

## Estimated Timing

Minimum time: 5-6 minutes.

Comfortable time with demo: 7-8 minutes.

## Slide 1: Project Title

Title: Fact Checking Agentic System

What to say:

This project is an AI-powered fact-checking system. The goal is to verify user-provided claims using evidence, instead of trusting the LLM's memory directly.

## Slide 2: Problem

What to say:

LLMs can sound confident even when they are wrong. They may hallucinate facts, use outdated knowledge, or answer without evidence. For fact-checking, that is risky, so we need a more controlled system.

## Slide 3: Main Idea

What to say:

Our system does not ask the model to answer from memory. Instead, it retrieves evidence first, then asks the model to judge the claim using only that evidence.

Flow:

```text
Claim -> Evidence -> Model judgment -> Citation validation -> Final report
```

## Slide 4: Tools Used

What to say:

We used Python for backend logic, OpenAI for structured LLM reasoning, LangGraph for workflow orchestration, Gradio for the UI, Wikipedia and local evidence for retrieval, JSON schema for structured output, and Mermaid for architecture diagrams.

## Slide 5: Architecture

What to say:

The system is built as a LangGraph workflow. LangGraph helps us organize the fact-checking process as separate nodes. Each node has one responsibility, and the output of one node becomes the input for the next node.

This makes the system easier to understand, debug, and improve. Instead of writing one large function or one large prompt, we split the work into smaller steps.

Flow:

```text
Validate input
-> Decompose claim
-> Retrieve evidence
-> Check subclaims
-> Validate citations
-> Aggregate verdict
-> Build final report
```

LangGraph nodes:

```text
validate_input
```

This is the first guardrail. It checks whether the user entered a factual claim. If the user enters a question, the system stops early and asks the user to rewrite it as a claim.

Example:

```text
Who won the FIFA 2026 World Cup?
```

This is a question, so the system returns `input_required`.

```text
decompose_claim
```

This node breaks a complex claim into smaller subclaims. This is useful because one user input may contain multiple facts.

Example:

```text
The Eiffel Tower is in Paris and Mars is known as the Red Planet.
```

This can become two subclaims:

```text
The Eiffel Tower is in Paris.
Mars is known as the Red Planet.
```

```text
check_subclaims
```

This node retrieves evidence for each subclaim. Then it asks OpenAI to check the subclaim using only the retrieved evidence. The model returns a structured result with verdict, confidence, explanation, and citation IDs.

```text
aggregate_verdict
```

This node combines all subclaim verdicts into one final verdict. For example, if one subclaim is supported and another is contradicted, the final result can become `partially_supported`.

This step is rule-based, not another model call.

```text
build_report
```

This node creates the final structured report. The report includes the original claim, final verdict, final reason, subclaims, evidence, explanations, citations, and citation validation status.

Simple way to explain in presentation:

The architecture is like an assembly line. The user gives a claim, the system checks whether it is valid input, breaks it into smaller claims, finds evidence, asks the model to judge using that evidence, validates citations, combines the results, and finally shows a readable report in Gradio.

## Slide 6: Guardrails

What to say:

We added guardrails to reduce unreliable behavior. The system checks if the input is a factual claim, forces structured JSON output, asks the model to use only retrieved evidence, and validates citation IDs.

Example:

If the user asks:

```text
Who won the FIFA 2026 World Cup?
```

the system asks them to rewrite it as a factual claim.

## Slide 7: Retrieval

What to say:

We started with a small local evidence store. Then we added Wikipedia fallback, so the system can find evidence for claims not present locally. We also improved retrieval when dates or numbers conflict.

Example:

```text
California's capital is Sacramento.
```

This can use Wikipedia if local evidence does not contain it.

## Slide 8: Evaluation

What to say:

We evaluate the system using test claims. The main metric is final verdict accuracy. We also inspect citation validation and retrieval source usage.

Important explanation:

Evaluation is for developers, not end users. A user checks one claim, but developers test many claims to measure reliability.

## Slide 9: Demo

Demo claims to try:

```text
California's capital is Sacramento.
The USA won the FIFA 2022 World Cup.
Coffee was first discovered in Brazil.
Who won the FIFA 2026 World Cup?
```

What to show:

Supported, contradicted, uncertain, and guardrail behavior.

## Slide 10: Limitations

What to say:

This is not production-ready yet. It still depends on available evidence, Wikipedia may not be enough for all domains, and subjective claims are hard to verify.

## Slide 11: Future Work

What to say:

In the future, we can add better source-specific APIs like CDC for health, SEC for finance, and official sports APIs. We can also add stronger prompt-injection protection, better source ranking, and more evaluation metrics.

## Slide 12: Conclusion

What to say:

This project helped us understand how to make LLMs more reliable by combining prompting, structured output, retrieval, validation, evaluation, and agentic workflow design.

## Short Version For 4-5 Minutes

If time is short, focus on these points:

1. LLMs can hallucinate, so we should not trust memory-only answers.
2. Our system retrieves evidence first.
3. OpenAI checks the claim using only that evidence.
4. LangGraph organizes the steps.
5. Gradio gives us a simple UI for testing.
6. Guardrails and citation validation make the output more reliable.
7. Evaluation helps developers measure whether the system is improving.
