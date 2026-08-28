def aggregate_final_verdict(subclaim_results):
    verdicts = [
        item["fact_check"].get("verdict")
        for item in subclaim_results
    ]

    if not verdicts:
        return {
            "final_verdict": "uncertain",
            "reason": "No subclaims were available to verify.",
        }

    if all(verdict == "contradicted" for verdict in verdicts):
        return {
            "final_verdict": "contradicted",
            "reason": "All subclaims were contradicted by the evidence.",
        }

    if "contradicted" in verdicts and "supported" in verdicts:
        return {
            "final_verdict": "partially_supported",
            "reason": (
                "Some subclaims were supported, but at least one subclaim was "
                "contradicted by the evidence."
            ),
        }

    if "contradicted" in verdicts:
        return {
            "final_verdict": "contradicted",
            "reason": "At least one subclaim was contradicted and none were supported.",
        }

    if "not_enough_evidence" in verdicts:
        return {
            "final_verdict": "uncertain",
            "reason": "At least one subclaim did not have enough evidence.",
        }

    if all(verdict == "supported" for verdict in verdicts):
        return {
            "final_verdict": "supported",
            "reason": "All subclaims were supported by the evidence.",
        }

    return {
        "final_verdict": "uncertain",
        "reason": "The subclaim verdicts could not be combined confidently.",
    }
