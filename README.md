# Fact Checking Agentic System

Beginner-friendly project for learning how to build a fact-checking agent step by step.

## Project Summary

This project builds an AI-powered fact-checking agent that verifies user-provided claims using external evidence instead of relying only on the model's internal knowledge. The system accepts a claim, breaks it into smaller checkable subclaims, retrieves relevant evidence, asks an LLM to judge each subclaim using only that evidence, validates citations, aggregates subclaim verdicts, and returns a structured final report.

The main goal is to reduce common LLM reliability issues such as hallucination, unsupported reasoning, and overconfident answers. Instead of asking the model to directly answer whether a claim is true, the system uses a controlled workflow:

```text
claim
-> decompose into subclaims
-> retrieve evidence
-> fact-check each subclaim with citations
-> validate citation IDs
-> aggregate final verdict
-> show structured report in UI
```

The current prototype supports local demo evidence first and uses Wikipedia retrieval as a fallback when local evidence is not available. The user-facing app checks one claim at a time, while the evaluation script tests multiple known examples to measure whether system changes improve reliability.

## Current Workflow

1. **User enters a claim**
   The user enters a claim in the Gradio UI.

2. **Claim decomposition**
   OpenAI structured output breaks complex claims into smaller factual subclaims.

3. **Evidence retrieval**
   The system first searches a local evidence store. If no local evidence is found, it retrieves evidence from Wikipedia and keeps real page URLs.

4. **Subclaim fact-checking**
   Each subclaim is checked against retrieved evidence. The model must return a structured verdict, confidence, explanation, and citation IDs.

5. **Citation validation**
   Python code verifies that every citation ID returned by the model exists in the retrieved evidence.

6. **Final verdict aggregation**
   Rule-based logic combines subclaim verdicts into one final verdict such as `supported`, `contradicted`, `partially_supported`, or `uncertain`.

7. **Structured final report**
   The system returns a JSON report and a readable Markdown report showing verdicts, explanations, retrieved evidence, source metadata, and citation validation.

8. **Evaluation**
   A developer evaluation script runs multiple known examples and measures final verdict accuracy, citation validation rate, and retrieval source usage.

## Tech Stack

| Tool | Purpose in this project |
| --- | --- |
| **Python** | Core application logic, retrieval, validation, aggregation, evaluation scripts, and package structure |
| **OpenAI Platform** | LLM calls for claim decomposition and evidence-grounded fact-checking with structured JSON outputs |
| **Gradio** | Browser-based demo UI where a user enters a claim and sees the final report |
| **LangGraph** | Agent workflow orchestration using graph nodes such as `decompose_claim`, `check_subclaims`, `aggregate_verdict`, and `build_report` |
| **Wikipedia API** | First real external retrieval source with page titles, summaries, and URLs |
| **Mermaid** | Architecture/workflow diagram for explaining the system visually |
| **Git/GitHub** | Version control for saving project progress and changes |

## Project Structure

```text
fact_checker/
  aggregation.py   # combines subclaim verdicts into final verdict
  evidence.py      # local demo evidence store
  graph.py         # LangGraph workflow
  llm.py           # OpenAI structured output calls
  reporting.py     # readable Markdown report formatting
  retrieval.py     # local retrieval and scoring
  validation.py    # citation validation
  wikipedia.py     # Wikipedia retrieval

demos/
  session_*.py     # step-by-step learning demos

docs/
  session-*.md     # beginner-friendly session notes
```

## Run The Current App

```bash
cd /Users/aishwarya/Documents/AI-Projects/fact-checking-agent
export OPENAI_API_KEY="your_api_key_here"
python3 demos/session_18_langgraph_gradio_app.py
```

Then open:

```text
http://127.0.0.1:50993
```

## Run The Evaluation

```bash
cd /Users/aishwarya/Documents/AI-Projects/fact-checking-agent
export OPENAI_API_KEY="your_api_key_here"
python3 demos/session_27_evaluate_langgraph_pipeline.py
```

## Learning Log

We will not jump straight into a large agent. First we build the mental model:

1. Why LLMs can be unreliable by default
2. How prompting changes behavior
3. How structured outputs make results easier to check
4. How evaluation tells us whether the system is improving
5. How retrieval gives the model external evidence
6. How to combine these ideas into a fact-checking agent

## Session 1

Start here:

```bash
python3 demos/session_01_stochastic_prompting.py
```

Then read:

- `docs/session-01-foundations.md`

This first demo uses a tiny simulated model instead of a real LLM API. That is intentional: it lets us understand the core idea without setup friction or costs.

## Session 2

Run the first tiny fact-checking prototype:

```bash
python3 demos/session_02_tiny_fact_checker.py
```

This demo still does not use an LLM. It shows the basic system shape:

```text
claim + evidence -> structured verdict
```

## Session 3

Run the first evaluation:

```bash
python3 demos/session_03_evaluate_tiny_fact_checker.py
```

This checks whether the tiny fact checker returns the expected verdicts.

## Session 4

Run the first OpenAI API version:

```bash
python3 demos/session_04_openai_structured_fact_checker.py
```

This version asks an LLM to produce the same structured verdict JSON. You need an OpenAI API key in your environment:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Optional:

```bash
export OPENAI_MODEL="gpt-5.6-luna"
```

## Session 5

Evaluate the OpenAI API version:

```bash
python3 demos/session_05_evaluate_openai_fact_checker.py
```

This runs multiple examples through the LLM and compares each verdict with the expected verdict.

## Session 6

Validate the OpenAI output shape:

```bash
python3 demos/session_06_validate_openai_output.py
```

This checks whether the model output is usable by code: required fields, allowed verdict, confidence range, and non-empty explanation.

## Session 7

Check whether explanations are grounded in the evidence:

```bash
python3 demos/session_07_groundedness_check.py
```

This adds a simple groundedness heuristic: does the explanation reuse meaningful words from the evidence?

## Session 8

Use multiple evidence snippets and citation IDs:

```bash
python3 demos/session_08_cited_fact_checker.py
```

This teaches the model to return `citation_ids`, so we can see which evidence item supports the verdict.

## Session 9

Validate citation IDs:

```bash
python3 demos/session_09_validate_citations.py
```

This checks whether every returned citation ID exists in the evidence items we provided.

## Session 10

Retrieve evidence from a tiny local evidence store:

```bash
python3 demos/session_10_local_retrieval.py
```

This introduces the retrieval step:

```text
claim -> retrieve relevant evidence -> model verdict with citations
```

## Session 11

Evaluate the retrieval pipeline:

```bash
python3 demos/session_11_evaluate_retrieval_pipeline.py
```

This measures both retrieval hit rate and verdict accuracy.

## Session 12

Decompose a complex claim into smaller subclaims:

```bash
python3 demos/session_12_claim_decomposition.py
```

This introduces the first planning-style step:

```text
complex claim -> smaller checkable claims
```

## Session 13

Run the first mini agent pipeline:

```bash
python3 demos/session_13_mini_agent_pipeline.py
```

This combines decomposition, retrieval, cited fact-checking, and citation validation.

## Session 14

Aggregate subclaim verdicts into one final verdict:

```bash
python3 demos/session_14_aggregate_final_verdict.py
```

This adds the final decision step:

```text
subclaim verdicts -> overall claim verdict
```

## Session 15

Build a structured final report:

```bash
python3 demos/session_15_structured_final_report.py
```

This returns one clean JSON report with the original claim, final verdict, subclaim results, evidence, citations, and validation status.

## Session 16

Open a simple Gradio UI:

```bash
python3 demos/session_16_gradio_app.py
```

This gives the project a small browser interface:

```text
user enters claim -> pipeline runs -> UI shows final report
```

## Session 17

Run the LangGraph workflow version:

```bash
python3 demos/session_17_langgraph_workflow.py
```

This converts the pipeline into graph nodes:

```text
decompose_claim -> check_subclaims -> aggregate_verdict -> build_report
```

## Session 18

Open the LangGraph-powered Gradio UI:

```bash
python3 demos/session_18_langgraph_gradio_app.py
```

This runs the browser demo through the LangGraph workflow instead of the earlier direct Python pipeline.

## Session 19

Review the Mermaid workflow diagram:

- `docs/session-19-mermaid-architecture.md`

This documents the current agent workflow visually.

## Session 20

Add citation source metadata:

- local evidence items now include `title`, `source_type`, and `url`
- the LangGraph Gradio UI shows source metadata in the readable report

## Session 21

Add source quality metadata:

- local evidence items now include `source_quality` and `source_score`
- the LangGraph Gradio UI shows source quality in the readable report

## Session 22

Use source quality in retrieval ranking:

- retrieval still depends mainly on word overlap
- `source_score` now nudges ranking when sources are similarly relevant

## Session 23

Design web retrieval:

- `docs/session-23-web-retrieval-design.md`

This plans how we will move from local demo evidence to real web evidence with URLs and source quality rules.

## Session 24

Retrieve evidence from Wikipedia:

```bash
python3 demos/session_24_wikipedia_retrieval.py
```

This is the first real web retrieval demo. It searches Wikipedia and converts results into our evidence format.

## Session 25

Use Wikipedia as retrieval fallback:

- LangGraph uses local retrieval first
- if no local evidence is found, it retrieves Wikipedia evidence
- the Gradio readable report shows whether evidence came from `local` or `wikipedia`

## Session 26

Add Gradio example claims:

- local retrieval example
- Wikipedia fallback example
- contradicted sports example
- not-enough-evidence example

## Session 27

Evaluate the current LangGraph pipeline:

```bash
python3 demos/session_27_evaluate_langgraph_pipeline.py
```

This measures final verdict accuracy, citation validation rate, and retrieval source usage.

## Session 28

Create a reusable `fact_checker/` package:

- old `demos/session_*.py` files remain as learning history
- reusable logic is copied into `fact_checker/`
- active Gradio and evaluation scripts now import from `fact_checker/`

## Session 29

Improve fallback for weak local retrieval:

- one generic word match no longer blocks Wikipedia fallback
- local graph retrieval now requires stronger overlap before using local evidence

## Session 30

Improve retrieval with number-aware scoring:

- retrieval extracts numbers from claims and evidence
- matching numbers boost retrieval score
- conflicting numbers are surfaced in retrieval diagnostics
- Gradio readable report now shows retrieval diagnostics

## Session 31

Broaden retrieval when number conflicts appear:

- if local evidence has a number conflict, the graph also retrieves Wikipedia evidence
- this gives the model stronger current evidence instead of only old local evidence
- retrieval source can now show `local+wikipedia`
