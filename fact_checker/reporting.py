def format_report_as_markdown(report):
    lines = [
        f"## Final Verdict: {report['final_verdict']}",
        "",
        f"**Reason:** {report['final_reason']}",
        "",
        "## Subclaims",
    ]

    for subclaim in report["subclaims"]:
        lines.extend(
            [
                "",
                f"### {subclaim['id']}: {subclaim['verdict']}",
                "",
                f"**Claim:** {subclaim['text']}",
                "",
                f"**Confidence:** {subclaim['confidence']}",
                "",
                f"**Explanation:** {subclaim['explanation']}",
                "",
                f"**Citations:** {', '.join(subclaim['citation_ids']) or 'None'}",
                "",
                f"**Citation validation:** {subclaim['citation_validation']}",
                "",
                f"**Retrieval source:** {subclaim.get('retrieval_source', 'unknown')}",
                "",
                "**Retrieved evidence:**",
            ]
        )

        for evidence in subclaim["retrieved_evidence"]:
            lines.append(
                f"- `{evidence['id']}` **{evidence.get('title', 'Untitled source')}** "
                f"({evidence.get('source_type', 'unknown')}): {evidence['text']}"
            )
            lines.append(f"  - Source: `{evidence.get('url', 'N/A')}`")
            lines.append(
                f"  - Quality: {evidence.get('source_quality', 'unknown')} "
                f"({evidence.get('source_score', 'N/A')})"
            )

        if subclaim.get("retrieval_diagnostics"):
            lines.append("")
            lines.append("**Retrieval diagnostics:**")
            for diagnostic in subclaim["retrieval_diagnostics"]:
                lines.append(
                    f"- `{diagnostic['evidence_id']}` score={diagnostic['combined_score']:.2f}, "
                    f"shared_words={diagnostic['shared_words']}, "
                    f"claim_numbers={diagnostic['claim_numbers']}, "
                    f"evidence_numbers={diagnostic['evidence_numbers']}, "
                    f"number_conflict={diagnostic['number_conflict']}"
                )

        if subclaim["citation_errors"]:
            lines.append("")
            lines.append("**Citation errors:**")
            for error in subclaim["citation_errors"]:
                lines.append(f"- {error}")

    return "\n".join(lines)
