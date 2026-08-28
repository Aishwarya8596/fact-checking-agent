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

    client = OpenAI()
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


def main():
    claim = "The Eiffel Tower is in Berlin."
    evidence_items = [
        {
            "id": "evidence_1",
            "text": "The Eiffel Tower is a landmark in Paris, France.",
        },
        {
            "id": "evidence_2",
            "text": "Berlin is the capital city of Germany.",
        },
    ]

    print("SESSION 8 DEMO: Cited fact checker")
    print("=" * 48)

    result = check_claim_with_citations(claim, evidence_items)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
