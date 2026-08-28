from session_04_openai_structured_fact_checker import check_claim_with_openai
from session_05_evaluate_openai_fact_checker import TEST_EXAMPLES


ALLOWED_VERDICTS = {"supported", "contradicted", "not_enough_evidence"}
REQUIRED_FIELDS = {"claim", "evidence", "verdict", "confidence", "explanation"}


def validate_fact_check_result(result):
    errors = []

    if not isinstance(result, dict):
        return ["Result must be a dictionary."]

    missing_fields = REQUIRED_FIELDS - set(result.keys())
    if missing_fields:
        errors.append(f"Missing required fields: {sorted(missing_fields)}")

    verdict = result.get("verdict")
    if verdict not in ALLOWED_VERDICTS:
        errors.append(f"Verdict must be one of: {sorted(ALLOWED_VERDICTS)}")

    confidence = result.get("confidence")
    if not isinstance(confidence, (int, float)):
        errors.append("Confidence must be a number.")
    elif not 0 <= confidence <= 1:
        errors.append("Confidence must be between 0 and 1.")

    for field_name in ["claim", "evidence", "explanation"]:
        value = result.get(field_name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field_name} must be a non-empty string.")

    return errors


def evaluate_with_validation():
    correct_count = 0
    valid_count = 0

    print("SESSION 6 DEMO: Validate OpenAI output")
    print("=" * 48)

    for example_number, example in enumerate(TEST_EXAMPLES, start=1):
        result = check_claim_with_openai(example["claim"], example["evidence"])
        validation_errors = validate_fact_check_result(result)
        is_valid = len(validation_errors) == 0

        actual_verdict = result.get("verdict")
        expected_verdict = example["expected_verdict"]
        is_correct = actual_verdict == expected_verdict

        if is_valid:
            valid_count += 1

        if is_correct:
            correct_count += 1

        verdict_status = "PASS" if is_correct else "FAIL"
        validation_status = "PASS" if is_valid else "FAIL"

        print(f"\nExample {example_number}")
        print(f"Verdict accuracy: {verdict_status}")
        print(f"Output validation: {validation_status}")
        print(f"Expected verdict: {expected_verdict}")
        print(f"Actual verdict:   {actual_verdict}")

        if validation_errors:
            print("Validation errors:")
            for error in validation_errors:
                print(f"- {error}")

    total_count = len(TEST_EXAMPLES)
    accuracy = correct_count / total_count
    validation_rate = valid_count / total_count

    print("\nSUMMARY")
    print("=" * 48)
    print(f"Verdict accuracy: {correct_count}/{total_count} ({accuracy:.1%})")
    print(f"Valid outputs:    {valid_count}/{total_count} ({validation_rate:.1%})")


if __name__ == "__main__":
    evaluate_with_validation()
