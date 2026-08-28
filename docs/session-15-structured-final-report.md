# Session 15: Structured Final Report

## What We Are Building

In Session 14, we created the final verdict.

In Session 15, we package everything into one structured report:

```text
original claim
final verdict
subclaim results
retrieved evidence
citations
validation status
```

## Why A Final Report Matters

Printing text is fine for learning.

But real applications need structured data.

For example, a Gradio UI could display:

1. The final verdict at the top.
2. Each subclaim in a table.
3. Retrieved evidence under each subclaim.
4. Citation validation warnings if something went wrong.

That is easier if our pipeline returns one predictable object.

## What The Report Looks Like

The report is JSON:

```json
{
  "original_claim": "...",
  "final_verdict": "supported",
  "final_reason": "...",
  "subclaims": [
    {
      "id": "subclaim_1",
      "text": "...",
      "verdict": "supported",
      "confidence": 0.9,
      "explanation": "...",
      "citation_ids": ["evidence_1"],
      "citation_validation": "passed",
      "retrieved_evidence": []
    }
  ]
}
```

## Why This Is A Good System Design Step

The project is becoming more modular:

```text
pipeline logic -> structured report -> UI / evaluation / saved logs
```

This means the UI does not need to know every internal detail. It can simply receive a report and display it.

## Key Takeaway

A reliable AI system should not only produce an answer.

It should produce an answer in a shape that other software can use, inspect, test, and display.
