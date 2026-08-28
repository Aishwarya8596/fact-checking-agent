from session_08_cited_fact_checker import check_claim_with_citations
from session_09_validate_citations import validate_citation_ids
from session_10_local_retrieval import LOCAL_EVIDENCE_STORE, retrieve_evidence


PIPELINE_TEST_EXAMPLES = [
    {
        "claim": "The Eiffel Tower is in Berlin.",
        "expected_verdict": "contradicted",
        "expected_evidence_ids": {"evidence_1"},
    },
    {
        "claim": "Mars is known as the Red Planet.",
        "expected_verdict": "supported",
        "expected_evidence_ids": {"evidence_3"},
    },
    {
        "claim": "Coffee was first discovered in Brazil.",
        "expected_verdict": "not_enough_evidence",
        "expected_evidence_ids": {"evidence_4"},
    },
]


def has_retrieval_hit(retrieved_evidence, expected_evidence_ids):
    retrieved_ids = {item["id"] for item in retrieved_evidence}
    return bool(retrieved_ids & expected_evidence_ids)


def evaluate_retrieval_pipeline():
    retrieval_hit_count = 0
    verdict_correct_count = 0
    citation_valid_count = 0

    print("SESSION 11 DEMO: Evaluate retrieval pipeline")
    print("=" * 48)

    for example_number, example in enumerate(PIPELINE_TEST_EXAMPLES, start=1):
        claim = example["claim"]
        retrieved_evidence = retrieve_evidence(claim, LOCAL_EVIDENCE_STORE)
        retrieval_hit = has_retrieval_hit(
            retrieved_evidence,
            example["expected_evidence_ids"],
        )

        result = check_claim_with_citations(claim, retrieved_evidence)
        citation_errors = validate_citation_ids(result, retrieved_evidence)

        actual_verdict = result.get("verdict")
        expected_verdict = example["expected_verdict"]
        verdict_correct = actual_verdict == expected_verdict
        citations_valid = len(citation_errors) == 0

        if retrieval_hit:
            retrieval_hit_count += 1
        if verdict_correct:
            verdict_correct_count += 1
        if citations_valid:
            citation_valid_count += 1

        retrieved_ids = [item["id"] for item in retrieved_evidence]

        print(f"\nExample {example_number}")
        print(f"Claim: {claim}")
        print(f"Retrieved IDs: {retrieved_ids}")
        print(f"Expected useful IDs: {sorted(example['expected_evidence_ids'])}")
        print(f"Retrieval hit: {'PASS' if retrieval_hit else 'FAIL'}")
        print(f"Expected verdict: {expected_verdict}")
        print(f"Actual verdict:   {actual_verdict}")
        print(f"Verdict accuracy: {'PASS' if verdict_correct else 'FAIL'}")
        print(f"Citation validation: {'PASS' if citations_valid else 'FAIL'}")

    total_count = len(PIPELINE_TEST_EXAMPLES)

    print("\nSUMMARY")
    print("=" * 48)
    print(
        f"Retrieval hit rate: {retrieval_hit_count}/{total_count} "
        f"({retrieval_hit_count / total_count:.1%})"
    )
    print(
        f"Verdict accuracy:   {verdict_correct_count}/{total_count} "
        f"({verdict_correct_count / total_count:.1%})"
    )
    print(
        f"Valid citations:    {citation_valid_count}/{total_count} "
        f"({citation_valid_count / total_count:.1%})"
    )


if __name__ == "__main__":
    evaluate_retrieval_pipeline()
