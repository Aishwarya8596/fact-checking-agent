import re

from session_04_openai_structured_fact_checker import check_claim_with_openai
from session_05_evaluate_openai_fact_checker import TEST_EXAMPLES
from session_06_validate_openai_output import validate_fact_check_result


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "because",
    "but",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "not",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "which",
}


def get_meaningful_words(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return {word for word in words if len(word) > 2 and word not in STOPWORDS}


def groundedness_score(evidence, explanation):
    evidence_words = get_meaningful_words(evidence)
    explanation_words = get_meaningful_words(explanation)

    if not explanation_words:
        return 0.0, set()

    shared_words = evidence_words & explanation_words
    score = len(shared_words) / len(explanation_words)

    return score, shared_words


def evaluate_with_groundedness():
    correct_count = 0
    valid_count = 0
    grounded_count = 0
    groundedness_threshold = 0.30

    print("SESSION 7 DEMO: Groundedness check")
    print("=" * 48)

    for example_number, example in enumerate(TEST_EXAMPLES, start=1):
        result = check_claim_with_openai(example["claim"], example["evidence"])

        validation_errors = validate_fact_check_result(result)
        is_valid = len(validation_errors) == 0

        actual_verdict = result.get("verdict")
        expected_verdict = example["expected_verdict"]
        is_correct = actual_verdict == expected_verdict

        score, shared_words = groundedness_score(
            example["evidence"],
            result.get("explanation", ""),
        )
        is_grounded = score >= groundedness_threshold

        if is_correct:
            correct_count += 1
        if is_valid:
            valid_count += 1
        if is_grounded:
            grounded_count += 1

        print(f"\nExample {example_number}")
        print(f"Verdict accuracy: {'PASS' if is_correct else 'FAIL'}")
        print(f"Output validation: {'PASS' if is_valid else 'FAIL'}")
        print(f"Groundedness:      {'PASS' if is_grounded else 'FAIL'}")
        print(f"Groundedness score: {score:.1%}")
        print(f"Shared words: {sorted(shared_words)}")
        print(f"Explanation: {result.get('explanation')}")

    total_count = len(TEST_EXAMPLES)

    print("\nSUMMARY")
    print("=" * 48)
    print(f"Verdict accuracy: {correct_count}/{total_count} ({correct_count / total_count:.1%})")
    print(f"Valid outputs:    {valid_count}/{total_count} ({valid_count / total_count:.1%})")
    print(f"Grounded outputs: {grounded_count}/{total_count} ({grounded_count / total_count:.1%})")


if __name__ == "__main__":
    evaluate_with_groundedness()
