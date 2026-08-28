import os
import sys
from pathlib import Path

import gradio as gr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fact_checker.graph import build_fact_check_graph
from fact_checker.reporting import format_report_as_markdown


EXAMPLE_CLAIM = (
    "The Eiffel Tower is in Paris, Berlin is the capital of Germany, "
    "and Mars is known as the Red Planet."
)

EXAMPLE_CLAIMS = [
    [
        "The Eiffel Tower is in Paris, Berlin is the capital of Germany, "
        "and Mars is known as the Red Planet."
    ],
    ["Argentina won the FIFA 2022 World Cup."],
    ["The USA won the FIFA 2022 World Cup."],
    ["Coffee was first discovered in Brazil."],
    ["Who won the FIFA 2026 World Cup?"],
]

FACT_CHECK_GRAPH = build_fact_check_graph()


def fact_check_claim_with_graph(claim):
    if not claim or not claim.strip():
        return "Please enter a claim.", "", "", {}

    try:
        final_state = FACT_CHECK_GRAPH.invoke({"claim": claim.strip()})
        report = final_state["report"]
    except SystemExit:
        return (
            "Setup error",
            "Check that OPENAI_API_KEY is set in the terminal running this app.",
            "",
            {},
        )
    except Exception as error:
        return "Error", str(error), "", {}

    readable_report = format_report_as_markdown(report)

    return report["final_verdict"], report["final_reason"], readable_report, report


def build_app():
    with gr.Blocks(title="Fact Checking Agent") as app:
        gr.Markdown("# Fact Checking Agent")
        gr.Markdown("LangGraph workflow version")

        claim_input = gr.Textbox(
            label="Claim",
            value=EXAMPLE_CLAIM,
            lines=4,
        )
        gr.Examples(
            examples=EXAMPLE_CLAIMS,
            inputs=claim_input,
        )

        run_button = gr.Button("Fact Check", variant="primary")

        final_verdict = gr.Textbox(label="Final Verdict")
        final_reason = gr.Textbox(label="Final Reason", lines=2)
        readable_report = gr.Markdown(label="Readable Report")
        report_output = gr.JSON(label="Structured Report")

        run_button.click(
            fn=fact_check_claim_with_graph,
            inputs=claim_input,
            outputs=[final_verdict, final_reason, readable_report, report_output],
        )

    return app


def main():
    app = build_app()
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "50993"))
    app.launch(server_port=server_port)


if __name__ == "__main__":
    main()
