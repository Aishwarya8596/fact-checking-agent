# Session 18: LangGraph Gradio UI

## What We Are Building

In Session 16, the Gradio app called our regular Python pipeline.

In Session 18, the Gradio app calls the LangGraph workflow:

```text
Gradio UI -> LangGraph workflow -> final report
```

## Why This Step Matters

This connects the class-demo UI to the agent workflow architecture.

The user experience stays simple:

```text
enter claim -> click Fact Check -> see final report
```

But internally, the work is now organized as graph nodes:

```text
decompose_claim -> check_subclaims -> aggregate_verdict -> build_report
```

## What Changed From Session 16?

Session 16:

```text
UI -> build_final_report()
```

Session 18:

```text
UI -> graph.invoke() -> report
```

The output still looks similar because the report shape is the same.

## Key Takeaway

The UI does not need to know every internal step.

It only needs to call the workflow and display the final report.
