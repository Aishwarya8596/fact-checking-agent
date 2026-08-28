# Session 28: Package Refactor

## What We Changed

Until now, most reusable logic lived in the `demos/` session files.

That was useful for learning step by step.

Now we created a reusable package:

```text
fact_checker/
```

## Why We Did This

The session files show the learning journey.

The package files represent the actual application code.

This gives us two layers:

```text
demos/        -> learning history
fact_checker/ -> reusable system code
```

## New Package Structure

```text
fact_checker/
  __init__.py
  aggregation.py
  evidence.py
  graph.py
  llm.py
  reporting.py
  retrieval.py
  validation.py
  wikipedia.py
```

## What The Active Scripts Use Now

The LangGraph Gradio app and evaluation script now import from:

```text
fact_checker.graph
fact_checker.reporting
```

This makes the app less dependent on earlier session files.

## Key Takeaway

We did not delete the demos.

We copied the reusable logic into a cleaner package so the project can keep growing without becoming tangled.
