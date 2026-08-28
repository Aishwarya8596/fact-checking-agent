import json
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from session_08_cited_fact_checker import check_claim_with_citations
from session_09_validate_citations import validate_citation_ids
from session_10_local_retrieval import LOCAL_EVIDENCE_STORE, retrieve_evidence
from session_12_claim_decomposition import decompose_claim_with_openai
from session_14_aggregate_final_verdict import aggregate_final_verdict
from session_24_wikipedia_retrieval import retrieve_wikipedia_evidence


class FactCheckState(TypedDict, total=False):
    claim: str
    original_claim: str
    subclaims: list[dict[str, str]]
    subclaim_results: list[dict[str, Any]]
    aggregation: dict[str, str]
    report: dict[str, Any]


def decompose_claim_node(state: FactCheckState) -> FactCheckState:
    decomposition = decompose_claim_with_openai(state["claim"])

    return {
        "original_claim": decomposition["original_claim"],
        "subclaims": decomposition["subclaims"],
    }


def check_subclaims_node(state: FactCheckState) -> FactCheckState:
    subclaim_results = []

    for subclaim in state["subclaims"]:
        subclaim_text = subclaim["text"]
        retrieved_evidence = retrieve_evidence(
            subclaim_text,
            LOCAL_EVIDENCE_STORE,
            top_k=2,
        )
        retrieval_source = "local"

        if not retrieved_evidence:
            retrieved_evidence = retrieve_wikipedia_evidence(subclaim_text, limit=2)
            retrieval_source = "wikipedia"

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
                "retrieval_source": retrieval_source,
                "retrieved_evidence": retrieved_evidence,
                "fact_check": fact_check_result,
                "citation_errors": citation_errors,
            }
        )

    return {"subclaim_results": subclaim_results}


def aggregate_verdict_node(state: FactCheckState) -> FactCheckState:
    aggregation = aggregate_final_verdict(state["subclaim_results"])
    return {"aggregation": aggregation}


def build_report_node(state: FactCheckState) -> FactCheckState:
    subclaim_reports = []

    for item in state["subclaim_results"]:
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
                "retrieval_source": item["retrieval_source"],
                "retrieved_evidence": item["retrieved_evidence"],
            }
        )

    aggregation = state["aggregation"]

    return {
        "report": {
            "original_claim": state["original_claim"],
            "final_verdict": aggregation["final_verdict"],
            "final_reason": aggregation["reason"],
            "subclaims": subclaim_reports,
        }
    }


def build_fact_check_graph():
    graph_builder = StateGraph(FactCheckState)

    graph_builder.add_node("decompose_claim", decompose_claim_node)
    graph_builder.add_node("check_subclaims", check_subclaims_node)
    graph_builder.add_node("aggregate_verdict", aggregate_verdict_node)
    graph_builder.add_node("build_report", build_report_node)

    graph_builder.add_edge(START, "decompose_claim")
    graph_builder.add_edge("decompose_claim", "check_subclaims")
    graph_builder.add_edge("check_subclaims", "aggregate_verdict")
    graph_builder.add_edge("aggregate_verdict", "build_report")
    graph_builder.add_edge("build_report", END)

    return graph_builder.compile()


def main():
    claim = (
        "The Eiffel Tower is in Paris, Berlin is the capital of Germany, "
        "and Mars is known as the Red Planet."
    )

    print("SESSION 17 DEMO: LangGraph workflow")
    print("=" * 48)

    graph = build_fact_check_graph()
    final_state = graph.invoke({"claim": claim})

    print(json.dumps(final_state["report"], indent=2))


if __name__ == "__main__":
    main()
