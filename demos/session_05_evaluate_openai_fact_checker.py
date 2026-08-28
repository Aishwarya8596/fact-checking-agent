from session_04_openai_structured_fact_checker import check_claim_with_openai


TEST_EXAMPLES = [
    {
        "claim": "The Eiffel Tower is in Berlin.",
        "evidence": "The Eiffel Tower is a landmark in Paris, France.",
        "expected_verdict": "contradicted",
    },
    {
        "claim": "Mars is known as the Red Planet.",
        "evidence": "Mars is often called the Red Planet because of its reddish appearance.",
        "expected_verdict": "supported",
    },
    {
        "claim": "Coffee was first discovered in Brazil.",
        "evidence": "Coffee is widely grown in Brazil today.",
        "expected_verdict": "not_enough_evidence",
    },
]


def evaluate():
    correct_count = 0

    print("SESSION 5 DEMO: Evaluate OpenAI fact checker")
    print("=" * 48)

    for example_number, example in enumerate(TEST_EXAMPLES, start=1):
        result = check_claim_with_openai(example["claim"], example["evidence"])
        actual_verdict = result["verdict"]
        expected_verdict = example["expected_verdict"]
        is_correct = actual_verdict == expected_verdict

        if is_correct:
            correct_count += 1

        status = "PASS" if is_correct else "FAIL"

        print(f"\nExample {example_number}: {status}")
        print(f"Claim: {example['claim']}")
        print(f"Expected verdict: {expected_verdict}")
        print(f"Actual verdict:   {actual_verdict}")
        print(f"Confidence:       {result['confidence']}")
        print(f"Explanation:      {result['explanation']}")

    total_count = len(TEST_EXAMPLES)
    accuracy = correct_count / total_count

    print("\nSUMMARY")
    print("=" * 48)
    print(f"Correct: {correct_count}/{total_count}")
    print(f"Accuracy: {accuracy:.1%}")


if __name__ == "__main__":
    evaluate()
