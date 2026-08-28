import json
import os
import sys


DEFAULT_MODEL = "gpt-5.6-luna"

FACT_CHECK_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "claim": {"type": "string"},
        "evidence": {"type": "string"},
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
    },
    "required": ["claim", "evidence", "verdict", "confidence", "explanation"],
}


def build_prompt(claim, evidence):
    return f"""
You are a careful fact-checking assistant.

Task:
Use only the provided evidence to classify the claim.

Allowed verdicts:
- supported: the evidence clearly supports the claim
- contradicted: the evidence clearly contradicts the claim
- not_enough_evidence: the evidence is related but does not prove or disprove the claim

Rules:
- Do not use outside knowledge.
- Do not guess.
- Keep the explanation short and based only on the evidence.

Claim:
{claim}

Evidence:
{evidence}
""".strip()


def check_claim_with_openai(claim, evidence):
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
        input=build_prompt(claim, evidence),
        reasoning={"effort": "low"},
        text={
            "format": {
                "type": "json_schema",
                "name": "fact_check_result",
                "schema": FACT_CHECK_SCHEMA,
                "strict": True,
            }
        },
    )

    return json.loads(response.output_text)


def main():
    claim = "The Eiffel Tower is in Berlin."
    evidence = "The Eiffel Tower is a landmark in Paris, France."

    print("SESSION 4 DEMO: OpenAI structured fact checker")
    print("=" * 48)

    result = check_claim_with_openai(claim, evidence)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
