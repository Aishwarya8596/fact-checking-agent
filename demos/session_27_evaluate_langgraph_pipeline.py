import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fact_checker.graph import build_fact_check_graph


EVALUATION_EXAMPLES = [
    {
        "claim": "The Eiffel Tower is in Paris.",
        "expected_final_verdict": "supported",
    },
    {
        "claim": "Argentina won the FIFA 2022 World Cup.",
        "expected_final_verdict": "supported",
    },
    {
        "claim": "The USA won the FIFA 2022 World Cup.",
        "expected_final_verdict": "contradicted",
    },
    {
        "claim": "Coffee was first discovered in Brazil.",
        "expected_final_verdict": "uncertain",
    },
]


def evaluate_langgraph_pipeline():
    graph = build_fact_check_graph()
    correct_count = 0
    valid_citation_count = 0
    total_subclaim_count = 0

    print("SESSION 27 DEMO: Evaluate LangGraph pipeline")
    print("=" * 48)

    for example_number, example in enumerate(EVALUATION_EXAMPLES, start=1):
        final_state = graph.invoke({"claim": example["claim"]})
        report = final_state["report"]

        actual_verdict = report["final_verdict"]
        expected_verdict = example["expected_final_verdict"]
        is_correct = actual_verdict == expected_verdict

        if is_correct:
            correct_count += 1

        retrieval_sources = []
        citation_statuses = []

        for subclaim in report["subclaims"]:
            total_subclaim_count += 1
            retrieval_sources.append(subclaim.get("retrieval_source", "unknown"))
            citation_statuses.append(subclaim["citation_validation"])

            if subclaim["citation_validation"] == "passed":
                valid_citation_count += 1

        print(f"\nExample {example_number}")
        print(f"Claim: {example['claim']}")
        print(f"Expected final verdict: {expected_verdict}")
        print(f"Actual final verdict:   {actual_verdict}")
        print(f"Verdict accuracy: {'PASS' if is_correct else 'FAIL'}")
        print(f"Retrieval sources: {retrieval_sources}")
        print(f"Citation validation: {citation_statuses}")

    total_examples = len(EVALUATION_EXAMPLES)
    final_verdict_accuracy = correct_count / total_examples
    citation_validation_rate = valid_citation_count / total_subclaim_count

    print("\nSUMMARY")
    print("=" * 48)
    print(
        f"Final verdict accuracy: {correct_count}/{total_examples} "
        f"({final_verdict_accuracy:.1%})"
    )
    print(
        f"Citation validation rate: {valid_citation_count}/{total_subclaim_count} "
        f"({citation_validation_rate:.1%})"
    )


if __name__ == "__main__":
    evaluate_langgraph_pipeline()
