# Session 16: Gradio UI

## What We Are Building

In Session 15, our pipeline returned a structured JSON report.

In Session 16, we show that report in a simple Gradio app:

```text
claim input -> run fact-checking pipeline -> display final verdict and report
```

## Why Add A UI?

A command-line demo is useful for developers.

But a class demo is easier to understand when someone can:

1. Paste a claim.
2. Click a button.
3. See the final verdict.
4. Inspect subclaims, evidence, explanations, and citations.

That is why we add Gradio.

## What Gradio Does

Gradio lets us build a small web interface in Python.

We do not need to build a full frontend with HTML, CSS, or JavaScript yet.

## What The UI Shows

The app shows:

1. The final verdict
2. The final reason
3. The complete JSON report

The JSON report is useful because it exposes the full internal workflow.

## Key Takeaway

The pipeline is now usable by a person, not only by a Python script.

This is an important step toward a presentable project demo.
