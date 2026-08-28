from session_08_cited_fact_checker import check_claim_with_citations
from session_09_validate_citations import validate_citation_ids
from session_10_local_retrieval import LOCAL_EVIDENCE_STORE, retrieve_evidence
from session_12_claim_decomposition import decompose_claim_with_openai


def run_fact_check_pipeline(claim):
    decomposition = decompose_claim_with_openai(claim)
    subclaim_results = []

    for subclaim in decomposition["subclaims"]:
        subclaim_text = subclaim["text"]
        retrieved_evidence = retrieve_evidence(
            subclaim_text,
            LOCAL_EVIDENCE_STORE,
            top_k=2,
        )
        fact_check_result = check_claim_with_citations(
            subclaim_text,
            retrieved_evidence,
        )
        citation_errors = validate_citation_ids(
            fact_check_result,
            retrieved_evidence,
        )

        subclaim_results.append(
            {
                "subclaim_id": subclaim["id"],
                "subclaim": subclaim_text,
                "retrieved_evidence": retrieved_evidence,
                "fact_check": fact_check_result,
                "citation_errors": citation_errors,
            }
        )

    return {
        "original_claim": decomposition["original_claim"],
        "subclaim_results": subclaim_results,
    }


def print_pipeline_report(pipeline_result):
    print("Original claim:")
    print(pipeline_result["original_claim"])

    for item in pipeline_result["subclaim_results"]:
        fact_check = item["fact_check"]
        citation_errors = item["citation_errors"]

        print("\n" + "-" * 48)
        print(f"{item['subclaim_id']}: {item['subclaim']}")

        print("\nRetrieved evidence:")
        for evidence_item in item["retrieved_evidence"]:
            print(f"- {evidence_item['id']}: {evidence_item['text']}")

        print("\nFact-check result:")
        print(f"Verdict: {fact_check.get('verdict')}")
        print(f"Confidence: {fact_check.get('confidence')}")
        print(f"Citation IDs: {fact_check.get('citation_ids')}")
        print(f"Explanation: {fact_check.get('explanation')}")
        print(f"Citation validation: {'PASS' if not citation_errors else 'FAIL'}")

        if citation_errors:
            print("Citation errors:")
            for error in citation_errors:
                print(f"- {error}")


def main():
    claim = (
        "The Eiffel Tower is in Paris, Berlin is the capital of Germany, "
        "and Mars is known as the Red Planet."
    )

    print("SESSION 13 DEMO: Mini agent pipeline")
    print("=" * 48)

    pipeline_result = run_fact_check_pipeline(claim)
    print_pipeline_report(pipeline_result)


if __name__ == "__main__":
    main()
