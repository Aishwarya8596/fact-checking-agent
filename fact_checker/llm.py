import json
import os
import sys


DEFAULT_MODEL = "gpt-5.6-luna"

CITED_FACT_CHECK_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "claim": {"type": "string"},
        "verdict": {
            "type": "string",
            "enum": ["supported", "contradicted", "not_enough_evidence"],
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
        },
        "explanation": {"type": "string"},
        "citation_ids": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["claim", "verdict", "confidence", "explanation", "citation_ids"],
}

CLAIM_DECOMPOSITION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "original_claim": {"type": "string"},
        "subclaims": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "text": {"type": "string"},
                },
                "required": ["id", "text"],
            },
        },
    },
    "required": ["original_claim", "subclaims"],
}


def require_openai_client():
    try:
        from openai import OpenAI
    except ImportError:
        print("Missing dependency: openai")
        print("Install it with: python3 -m pip install -r requirements.txt")
        sys.exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("Missing environment variable: OPENAI_API_KEY")
        print('Set it with: export OPENAI_API_KEY="your_api_key_here"')
        sys.exit(1)

    return OpenAI()


def format_evidence(evidence_items):
    formatted_items = []

    for item in evidence_items:
        formatted_items.append(f"{item['id']}: {item['text']}")

    return "\n".join(formatted_items)


def build_cited_prompt(claim, evidence_items):
    evidence_text = format_evidence(evidence_items)

    return f"""
You are a careful fact-checking assistant.

Task:
Use only the provided evidence items to classify the claim.

Allowed verdicts:
- supported: the evidence clearly supports the claim
- contradicted: the evidence clearly contradicts the claim
- not_enough_evidence: the evidence is related but does not prove or disprove the claim

Rules:
- Do not use outside knowledge.
- Do not guess.
- Choose citation_ids only from the evidence IDs shown below.
- If no evidence item is useful, return an empty citation_ids list.
- Keep the explanation short and based only on the cited evidence.

Claim:
{claim}

Evidence items:
{evidence_text}
""".strip()


def check_claim_with_citations(claim, evidence_items):
    client = require_openai_client()
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    response = client.responses.create(
        model=model,
        input=build_cited_prompt(claim, evidence_items),
        reasoning={"effort": "low"},
        text={
            "format": {
                "type": "json_schema",
                "name": "cited_fact_check_result",
                "schema": CITED_FACT_CHECK_SCHEMA,
                "strict": True,
            }
        },
    )

    return json.loads(response.output_text)


def build_decomposition_prompt(claim):
    return f"""
You are helping build a fact-checking system.

Task:
Break the claim into smaller factual subclaims.

Rules:
- Keep each subclaim atomic: one checkable idea per subclaim.
- Do not answer whether the claim is true.
- Do not add new facts.
- If the claim already has one simple fact, return one subclaim.
- Use IDs like subclaim_1, subclaim_2, subclaim_3.

Claim:
{claim}
""".strip()


def decompose_claim_with_openai(claim):
    client = require_openai_client()
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    response = client.responses.create(
        model=model,
        input=build_decomposition_prompt(claim),
        reasoning={"effort": "low"},
        text={
            "format": {
                "type": "json_schema",
                "name": "claim_decomposition",
                "schema": CLAIM_DECOMPOSITION_SCHEMA,
                "strict": True,
            }
        },
    )

    return json.loads(response.output_text)
