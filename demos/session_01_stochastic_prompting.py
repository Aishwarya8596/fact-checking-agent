import json
import random


PROMPT = "Tell me one reason fact checking is hard."

POSSIBLE_ANSWERS = [
    "Sources can disagree.",
    "Claims may depend on fresh information.",
    "The wording of a claim can be ambiguous.",
    "A claim can mix true and false details.",
]


def simulated_llm(prompt):
    """Return one plausible answer to mimic probabilistic generation."""
    if prompt != PROMPT:
        return "I am only prepared for the Session 1 demo prompt."

    return random.choice(POSSIBLE_ANSWERS)


def weak_prompt_demo():
    claim = "The Eiffel Tower is in Berlin."
    return f"Claim: {claim}\nAnswer: No, that sounds false."


def better_prompt_demo():
    claim = "The Eiffel Tower is in Berlin."
    evidence = "The Eiffel Tower is a landmark in Paris, France."

    return {
        "claim": claim,
        "evidence": evidence,
        "verdict": "contradicted",
        "confidence": 0.94,
        "explanation": (
            "The evidence says the Eiffel Tower is in Paris, France, "
            "not Berlin."
        ),
    }


def main():
    print("SESSION 1 DEMO: Stochastic-style outputs")
    print("=" * 48)
    print(f"Prompt: {PROMPT}\n")

    for run_number in range(1, 6):
        print(f"Run {run_number}: {simulated_llm(PROMPT)}")

    print("\nWEAK PROMPT DEMO")
    print("=" * 48)
    print(weak_prompt_demo())

    print("\nBETTER STRUCTURED OUTPUT DEMO")
    print("=" * 48)
    print(json.dumps(better_prompt_demo(), indent=2))


if __name__ == "__main__":
    main()
