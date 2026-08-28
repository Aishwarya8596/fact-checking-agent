import json
import os
import sys


DEFAULT_MODEL = "gpt-5.6-luna"

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


def main():
    claim = (
        "The Eiffel Tower is in Paris, Berlin is the capital of Germany, "
        "and Mars is known as the Red Planet."
    )

    print("SESSION 12 DEMO: Claim decomposition")
    print("=" * 48)

    result = decompose_claim_with_openai(claim)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
