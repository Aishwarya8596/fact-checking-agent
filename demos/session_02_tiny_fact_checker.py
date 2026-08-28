import json


def check_claim(claim, evidence):
    claim_lower = claim.lower()
    evidence_lower = evidence.lower()

    if "eiffel tower" in claim_lower and "berlin" in claim_lower:
        if "paris" in evidence_lower and "france" in evidence_lower:
            return {
                "claim": claim,
                "evidence": evidence,
                "verdict": "contradicted",
                "confidence": 0.95,
                "explanation": (
                    "The claim says the Eiffel Tower is in Berlin, but the "
                    "evidence says it is in Paris, France."
                ),
            }

    if "mars" in claim_lower and "red planet" in claim_lower:
        if "mars" in evidence_lower and "red planet" in evidence_lower:
            return {
                "claim": claim,
                "evidence": evidence,
                "verdict": "supported",
                "confidence": 0.92,
                "explanation": (
                    "The claim says Mars is called the Red Planet, and the "
                    "evidence says the same thing."
                ),
            }

    return {
        "claim": claim,
        "evidence": evidence,
        "verdict": "not_enough_evidence",
        "confidence": 0.4,
        "explanation": (
            "The evidence does not clearly support or contradict the claim "
            "using the simple rules in this demo."
        ),
    }


def main():
    examples = [
        {
            "claim": "The Eiffel Tower is in Berlin.",
            "evidence": "The Eiffel Tower is a landmark in Paris, France.",
        },
        {
            "claim": "Mars is known as the Red Planet.",
            "evidence": "Mars is often called the Red Planet because of its reddish appearance.",
        },
        {
            "claim": "Coffee was first discovered in Brazil.",
            "evidence": "Coffee is widely grown in Brazil today.",
        },
    ]

    print("SESSION 2 DEMO: Tiny fact checker")
    print("=" * 48)

    for example_number, example in enumerate(examples, start=1):
        result = check_claim(example["claim"], example["evidence"])
        print(f"\nExample {example_number}")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
