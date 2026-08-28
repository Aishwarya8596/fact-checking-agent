from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from fact_checker.aggregation import aggregate_final_verdict
from fact_checker.evidence import LOCAL_EVIDENCE_STORE
from fact_checker.input_guardrails import validate_fact_check_input
from fact_checker.llm import check_claim_with_citations, decompose_claim_with_openai
from fact_checker.retrieval import retrieve_evidence_with_diagnostics
from fact_checker.validation import validate_citation_ids
from fact_checker.wikipedia import retrieve_wikipedia_evidence


class FactCheckState(TypedDict, total=False):
    claim: str
    original_claim: str
    subclaims: list[dict[str, str]]
    subclaim_results: list[dict[str, Any]]
    aggregation: dict[str, str]
    report: dict[str, Any]
    input_is_valid: bool
    guardrail_reason: str


def validate_input_node(state: FactCheckState) -> FactCheckState:
    validation_result = validate_fact_check_input(state["claim"])

    return {
        "input_is_valid": validation_result["is_valid"],
        "guardrail_reason": validation_result["reason"],
    }


def choose_next_node_after_input_validation(state: FactCheckState) -> str:
    if state["input_is_valid"]:
        return "decompose_claim"

    return "build_guardrail_report"


def build_guardrail_report_node(state: FactCheckState) -> FactCheckState:
    return {
        "report": {
            "original_claim": state.get("claim", ""),
            "final_verdict": "input_required",
            "final_reason": state["guardrail_reason"],
            "subclaims": [],
        }
    }


def decompose_claim_node(state: FactCheckState) -> FactCheckState:
    decomposition = decompose_claim_with_openai(state["claim"])

    return {
        "original_claim": decomposition["original_claim"],
        "subclaims": decomposition["subclaims"],
    }


def has_number_conflict(retrieval_diagnostics):
    return any(
        diagnostic.get("number_conflict", False)
        for diagnostic in retrieval_diagnostics
    )


def merge_evidence(primary_evidence, supplemental_evidence):
    merged_evidence = []
    seen_ids = set()

    for evidence_item in primary_evidence + supplemental_evidence:
        evidence_id = evidence_item["id"]
        if evidence_id not in seen_ids:
            merged_evidence.append(evidence_item)
            seen_ids.add(evidence_id)

    return merged_evidence


def check_subclaims_node(state: FactCheckState) -> FactCheckState:
    subclaim_results = []

    for subclaim in state["subclaims"]:
        subclaim_text = subclaim["text"]
        retrieved_evidence, retrieval_diagnostics = retrieve_evidence_with_diagnostics(
            subclaim_text,
            LOCAL_EVIDENCE_STORE,
            top_k=2,
            min_relevance_score=2,
        )
        retrieval_source = "local"

        if not retrieved_evidence:
            retrieved_evidence = retrieve_wikipedia_evidence(subclaim_text, limit=2)
            retrieval_source = "wikipedia"
            retrieval_diagnostics = []
        elif has_number_conflict(retrieval_diagnostics):
            wikipedia_evidence = retrieve_wikipedia_evidence(subclaim_text, limit=2)
            retrieved_evidence = merge_evidence(retrieved_evidence, wikipedia_evidence)
            retrieval_source = "local+wikipedia"

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
                "retrieval_diagnostics": retrieval_diagnostics,
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
                "retrieval_diagnostics": item["retrieval_diagnostics"],
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

    graph_builder.add_node("validate_input", validate_input_node)
    graph_builder.add_node("decompose_claim", decompose_claim_node)
    graph_builder.add_node("check_subclaims", check_subclaims_node)
    graph_builder.add_node("aggregate_verdict", aggregate_verdict_node)
    graph_builder.add_node("build_report", build_report_node)
    graph_builder.add_node("build_guardrail_report", build_guardrail_report_node)

    graph_builder.add_edge(START, "validate_input")
    graph_builder.add_conditional_edges(
        "validate_input",
        choose_next_node_after_input_validation,
        {
            "decompose_claim": "decompose_claim",
            "build_guardrail_report": "build_guardrail_report",
        },
    )
    graph_builder.add_edge("decompose_claim", "check_subclaims")
    graph_builder.add_edge("check_subclaims", "aggregate_verdict")
    graph_builder.add_edge("aggregate_verdict", "build_report")
    graph_builder.add_edge("build_report", END)
    graph_builder.add_edge("build_guardrail_report", END)

    return graph_builder.compile()
