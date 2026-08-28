import json

from session_13_mini_agent_pipeline import run_fact_check_pipeline
from session_14_aggregate_final_verdict import aggregate_final_verdict


def build_final_report(claim):
    pipeline_result = run_fact_check_pipeline(claim)
    aggregation = aggregate_final_verdict(pipeline_result["subclaim_results"])

    subclaim_reports = []

    for item in pipeline_result["subclaim_results"]:
        fact_check = item["fact_check"]
        citation_errors = item["citation_errors"]

        subclaim_reports.append(
            {
                "id": item["subclaim_id"],
                "text": item["subclaim"],
                "verdict": fact_check.get("verdict"),
                "confidence": fact_check.get("confidence"),
                "explanation": fact_check.get("explanation"),
                "citation_ids": fact_check.get("citation_ids"),
                "citation_validation": "failed" if citation_errors else "passed",
                "citation_errors": citation_errors,
                "retrieved_evidence": item["retrieved_evidence"],
            }
        )

    return {
        "original_claim": pipeline_result["original_claim"],
        "final_verdict": aggregation["final_verdict"],
        "final_reason": aggregation["reason"],
        "subclaims": subclaim_reports,
    }


def main():
    claim = (
        "The Eiffel Tower is in Paris, Berlin is the capital of Germany, "
        "and Mars is known as the Red Planet."
    )

    print("SESSION 15 DEMO: Structured final report")
    print("=" * 48)

    report = build_final_report(claim)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
