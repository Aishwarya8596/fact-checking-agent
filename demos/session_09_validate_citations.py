from session_08_cited_fact_checker import check_claim_with_citations


def validate_citation_ids(result, evidence_items):
    errors = []

    citation_ids = result.get("citation_ids")
    if not isinstance(citation_ids, list):
        return ["citation_ids must be a list."]

    allowed_ids = {item["id"] for item in evidence_items}

    for citation_id in citation_ids:
        if not isinstance(citation_id, str):
            errors.append("Every citation ID must be a string.")
        elif citation_id not in allowed_ids:
            errors.append(f"Unknown citation ID: {citation_id}")

    return errors


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

    print("SESSION 9 DEMO: Validate citations")
    print("=" * 48)

    result = check_claim_with_citations(claim, evidence_items)
    citation_errors = validate_citation_ids(result, evidence_items)
    citation_status = "PASS" if not citation_errors else "FAIL"

    print(f"Verdict: {result.get('verdict')}")
    print(f"Citation IDs: {result.get('citation_ids')}")
    print(f"Citation validation: {citation_status}")

    if citation_errors:
        print("Citation errors:")
        for error in citation_errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
