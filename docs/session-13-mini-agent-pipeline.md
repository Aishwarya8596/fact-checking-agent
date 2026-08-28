# Session 13: Mini Agent Pipeline

## What We Are Building

In this session, we combine the pieces from earlier sessions:

```text
complex claim
-> decompose into subclaims
-> retrieve evidence for each subclaim
-> fact-check each subclaim
-> validate citations
-> print a report
```

This is our first small agentic workflow.

## Why This Is Different

Earlier demos focused on one skill at a time:

1. Structured output
2. Evaluation
3. Validation
4. Citations
5. Retrieval
6. Decomposition

Now we connect them.

Each step produces output that becomes input for the next step.

## The Pipeline

### Step 1: Decompose

The model breaks a complex claim into smaller subclaims.

### Step 2: Retrieve

For each subclaim, our local retriever finds relevant evidence from the local evidence store.

### Step 3: Verify

The model checks each subclaim using only the retrieved evidence.

### Step 4: Validate

Code checks whether the returned citation IDs are real evidence IDs.

### Step 5: Report

The script prints a readable summary of each subclaim and verdict.

## Why This Matters

This pattern is the heart of our fact-checking agent:

```text
do not answer directly
break the task down
collect evidence
reason using evidence
validate the output
```

## Key Takeaway

An agentic system is not just one model call.

It is a controlled workflow where model calls and code checks work together.
